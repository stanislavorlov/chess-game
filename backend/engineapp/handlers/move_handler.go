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

	moveValidationResult := game.MovePiece(msg)
	log.Printf("[Game: %s] Local move validation result for %s -> %s: %v", gameID, msg.From, msg.To, moveValidationResult.Valid)

	// If validation fails, restore the pre-move state and publish it back

	/*var state uint8
	if game.IsCheck() {
		state |= 1 // bit 0: check
	}
	if game.IsCheckmate() {
		state |= 1 << 1 // bit 1: checkmate
	}
	if game.IsStalemate() {
		state |= 1 << 2 // bit 2: stalemate
	}
	if game.IsDraw() {
		state |= 1 << 3 // bit 3: draw
	}
	if game.Turn() == "b" {
		state |= 1 << 4 // bit 4: turn (0=w, 1=b)
	}
	if game.Winner() == "b" {
		state |= 1 << 5 // bit 5: winner is black
	} else if game.Winner() == "w" {
		state |= 1 << 6 // bit 6: winner is white
	}*/
	var state uint8 = PackGameState(game)

	if !moveValidationResult.Valid {
		log.Printf("[Game: %s] Warning: Move rejected by local validation logic.", gameID)

		/*resp := ws.GameResponse{
			Fen:        EncodeFENTo34Bytes(game.FEN()),
			LastMove:   msg.From + "-" + msg.To,
			LegalMoves: game.LegalMoves(),
			Turn:       game.Turn(),
			State: ws.GameState{
				IsCheck:     game.IsCheck(),
				IsCheckmate: game.IsCheckmate(),
				IsStalemate: game.IsStalemate(),
				IsDraw:      game.IsDraw(),
			},
		}*/

		game_update := ws.GameUpdate{
			GameID:    gameID,
			EventType: "game_update",
			Data: ws.GameUpdateData{
				Fen:      PackFenToBytes(game.FEN()),
				LastMove: msg.From + msg.To,
				State:    state,
			},
		}

		/*{
		"event": "game_update",
		"data": {
			"fen": "r1bqkbnr/pppp1Qpp/2n5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4",
			"last_move": "f7f7",
			"state": 111111  //in_check,is_checkmate,is_stalemate,is_draw,turn,winner
		}
		} */

		if responseBytes, err := json.Marshal(game_update); err == nil {
			send(responseBytes)
		} else {
			log.Printf("Error marshaling move response: %v", err)
		}
		return
	}

	// Apply AI move, update the state and publish it back

	game_update := ws.GameUpdate{
		GameID:    gameID,
		EventType: "game_update",
		Data: ws.GameUpdateData{
			Fen:      PackFenToBytes(game.FEN()),
			LastMove: msg.From + msg.To,
			State:    state,
		},
	}

	/*resp := ws.GameResponse{
		Fen:        EncodeFENTo34Bytes(game.FEN()),
		LastMove:   msg.From + "-" + msg.To,
		LegalMoves: game.LegalMoves(),
		Turn:       game.Turn(),
		State: ws.GameState{
			IsCheck:     game.IsCheck(),
			IsCheckmate: game.IsCheckmate(),
			IsStalemate: game.IsStalemate(),
			IsDraw:      game.IsDraw(),
		},
	}*/

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
