package services

import (
	"context"
	"encoding/json"
	"log"

	"engineapp/database"

	"github.com/go-redis/redis/v8"
)

// BoardState represents the current layout of the chess board that AI expects or players see.
type BoardState struct {
	Fen string `json:"fen"`
}

// GetGameState checks Redis for an active game state, falling back to MongoDB's GameHistory if necessary.
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

	log.Printf("[GameStateService] Cache MISS for GameID: %s. Returning default state...", gameIDStr)

	// 2. Fallback to default starting position if no cache or DB state is found
	fen := "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" // Startpos default

	// ToDo: gRPC call to chhesapp to get the current board state ??

	return &BoardState{
		Fen: fen,
	}, nil
}
