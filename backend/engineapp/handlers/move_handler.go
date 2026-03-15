package handlers

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"time"

	"engineapp/handlers/ws"
	pb "engineapp/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

// HandleMove processes an incoming move message for a given game
func HandleMove(gameID string, message []byte) []byte {
	var msg ws.MoveMessage
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return nil
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	// Call Python chessapp via gRPC for AI move
	grpcHost := os.Getenv("CHESSAPP_GRPC_HOST")
	if grpcHost == "" {
		grpcHost = "localhost:50052"
	}

	conn, err := grpc.NewClient(grpcHost, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("Failed to connect to chessapp gRPC: %v", err)
	} else {
		defer conn.Close()
		client := pb.NewAiServiceClient(conn)

		ctx, cancel := context.WithTimeout(context.Background(), time.Second)
		defer cancel()

		predictResp, err := client.GetPredictedMove(ctx, &pb.PredictedMoveRequest{
			Bitboard:    "dummy_bitboard_placeholder",
			IsWhiteTurn: true,
		})

		if err != nil {
			log.Printf("Failed to call GetPredictedMove via gRPC: %v", err)
		} else {
			log.Printf("Received Predicted Move from Python gRPC: uci_move=%s", predictResp.UciMove)
		}
	}

	// Create mock response
	resp := ws.MoveResponse{
		Type:    "move_validation",
		IsValid: true,
		Move:    msg.From + msg.To, // e.g. "e2e4"
		From:    msg.From,
		To:      msg.To,
	}

	responseBytes, err := json.Marshal(resp)
	if err != nil {
		log.Printf("Error marshaling move response: %v", err)
		return nil
	}

	return responseBytes
}
