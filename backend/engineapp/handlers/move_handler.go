package handlers

import (
	"context"
	"encoding/json"
	"log"

	"engineapp/database"
	"engineapp/handlers/ws"
	"engineapp/services"
)

// MoveHandler manages move-related requests and their dependencies.
type MoveHandler struct {
	Repo *database.MongoRepository
}

// NewMoveHandler creates a new MoveHandler instance.
func NewMoveHandler(repo *database.MongoRepository) *MoveHandler {
	return &MoveHandler{Repo: repo}
}

// HandleMove processes an incoming move message for a given game
func (h *MoveHandler) HandleMove(gameID string, message []byte, send func([]byte)) {
	var msg ws.GameRequest
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	game, err := h.Repo.GetGame(context.Background(), gameID)
	if err != nil {
		log.Printf("[Game: %s] Failed to get Game: %v", gameID, err)
		return
	}

	movePieceResult := game.MovePiece(msg)
	log.Printf("[Game: %s] Local move validation result for %s -> %s: %v", gameID, msg.From, msg.To, movePieceResult.Valid)

	// If validation fails, restore the pre-move state and publish it back
	var state uint8 = PackGameState(game)

	if !movePieceResult.Valid {
		log.Printf("[Game: %s] Warning: Move rejected by local validation logic.", gameID)

		game_update := ws.GameUpdate{
			EventType: "game_update",
			Data: ws.GameUpdateData{
				Fen:      PackFenToBytes(game.FEN()),
				LastMove: msg.From + msg.To,
				State:    state,
			},
		}

		if responseBytes, err := json.Marshal(game_update); err == nil {
			send(responseBytes)
		} else {
			log.Printf("Error marshaling move response: %v", err)
		}
		return
	}

	// Apply AI move, update the state and publish it back

	game_update := ws.GameUpdate{
		EventType: "game_update",
		Data: ws.GameUpdateData{
			Fen:      PackFenToBytes(game.FEN()),
			LastMove: msg.From + msg.To,
			State:    state,
		},
	}

	// 1. Synchronously publish the move validation result
	resp1Bytes, _ := json.Marshal(game_update)
	send(resp1Bytes)

	// 2. Asynchronously request AI prediction and publish it
	go func() {
		predictedMoveUci, err := services.PredictMove(context.Background(), gameID, game.Bitboards)
		if err != nil {
			log.Printf("Failed to get predicted move: %v", err)
			return
		}

		// Publish AI move prediction
		resp2Bytes, _ := json.Marshal(ws.AIPredictedMove{
			GameID:          gameID,
			PredictedAiMove: predictedMoveUci,
			EventType:       "ai-predicted-move",
		})
		send(resp2Bytes)
	}()
}
