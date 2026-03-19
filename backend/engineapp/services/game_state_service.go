package services

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"time"

	"engineapp/database"
	pb "engineapp/proto"

	"github.com/go-redis/redis/v8"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// BoardState represents the current layout of the chess board that AI expects or players see.
type BoardState struct {
	Fen string `json:"fen"`
}

// GetGameState checks Redis for an active game state, falling back to FastAPI gRPC if necessary.
func GetGameState(ctx context.Context, gameIDStr string) (*BoardState, error) {
	// 1. Check Redis Cache
	cachedState, err := database.GetGameState(ctx, gameIDStr)
	if err == nil && cachedState != "" {
		log.Printf("[GameStateService] Cache HIT for GameID: %s", gameIDStr)
		var state BoardState
		if decodeErr := json.Unmarshal([]byte(cachedState), &state); decodeErr == nil {
			return &state, nil
		}
		log.Printf("[GameStateService] Failed to decode Redis cache for GameID: %s.", gameIDStr)
	} else if err != redis.Nil {
		log.Printf("[GameStateService] Redis error for GameID %s: %v", gameIDStr, err)
	}

	log.Printf("[GameStateService] Cache MISS for GameID: %s. Fetching via gRPC...", gameIDStr)

	// 2. Fallback to gRPC call to chhesapp to get the current board state
	grpcHost := os.Getenv("CHESSAPP_GRPC_HOST")
	if grpcHost == "" {
		grpcHost = "localhost:50052"
	}

	conn, err := grpc.NewClient(grpcHost, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("[GameStateService] Failed to connect to chessapp gRPC: %v", err)
	} else {
		defer conn.Close()
		client := pb.NewGameStateClient(conn)

		rpcCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
		defer cancel()

		resp, err := client.GetState(rpcCtx, &pb.GameStateRequest{GameId: gameIDStr})
		if err != nil {
			log.Printf("[GameStateService] gRPC GetState failed: %v", err)
		} else {
			log.Printf("[GameStateService] gRPC GetState SUCCESS: %s", resp.Fen)

			encodedStr, err := json.Marshal(BoardState{Fen: resp.Fen})
			if err != nil {
				log.Printf("[GameStateService] Failed to encode Redis cache for GameID: %s.", gameIDStr)
			}
			database.SetGameState(ctx, gameIDStr, string(encodedStr))

			return &BoardState{Fen: resp.Fen}, nil
		}
	}

	// 3. Fallback to default starting position if no cache or gRPC state is found
	fen := "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" // Startpos default

	return &BoardState{
		Fen: fen,
	}, nil
}
