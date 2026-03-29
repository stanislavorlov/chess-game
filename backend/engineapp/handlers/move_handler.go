package handlers

import (
	"context"
	"encoding/json"
	"log"

	"engineapp/database"
	"engineapp/handlers/ws"
	"engineapp/models"
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
func (h *MoveHandler) HandleMove(gameID string, message []byte) []byte {
	var msg ws.MoveMessage
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return nil
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	gameState, err := h.Repo.GetGameState(context.Background(), gameID)
	if err != nil {
		log.Printf("[Game: %s] Failed to get GameState: %v", gameID, err)
		return nil
	}

	if gameState.GameStatus != "active" {
		log.Printf("[Game: %s] Game is not active", gameID)
		return nil
	}

	history, err := h.Repo.GetGameHistory(context.Background(), gameID)
	if err != nil {
		log.Printf("[Game: %s] Failed to get GameHistory: %v", gameID, err)
		return nil
	}

	if len(history) == 0 {
		log.Printf("[Game: %s] No history found for game", gameID)
		return nil
	}

	// Get the last history entry (latest bitboard)
	latestEntry := &history[len(history)-1]

	bitboards, err := services.FENToBitboards(latestEntry.BoardFen)
	if err != nil {
		log.Printf("Failed to convert FEN to bitboards: %v", err)
		return nil
	}

	bbMap := make(map[models.PieceKey]uint64)
	bbMap[models.PieceKey{Side: models.White, PieceType: models.Pawn}] = bitboards.WhitePawns
	bbMap[models.PieceKey{Side: models.White, PieceType: models.Knight}] = bitboards.WhiteKnights
	bbMap[models.PieceKey{Side: models.White, PieceType: models.Bishop}] = bitboards.WhiteBishops
	bbMap[models.PieceKey{Side: models.White, PieceType: models.Rook}] = bitboards.WhiteRooks
	bbMap[models.PieceKey{Side: models.White, PieceType: models.Queen}] = bitboards.WhiteQueens
	bbMap[models.PieceKey{Side: models.White, PieceType: models.King}] = bitboards.WhiteKings

	bbMap[models.PieceKey{Side: models.Black, PieceType: models.Pawn}] = bitboards.BlackPawns
	bbMap[models.PieceKey{Side: models.Black, PieceType: models.Knight}] = bitboards.BlackKnights
	bbMap[models.PieceKey{Side: models.Black, PieceType: models.Bishop}] = bitboards.BlackBishops
	bbMap[models.PieceKey{Side: models.Black, PieceType: models.Rook}] = bitboards.BlackRooks
	bbMap[models.PieceKey{Side: models.Black, PieceType: models.Queen}] = bitboards.BlackQueens
	bbMap[models.PieceKey{Side: models.Black, PieceType: models.King}] = bitboards.BlackKings

	occupancies := make(map[models.Side]uint64)
	occupancies[models.White] = bitboards.WhitePawns | bitboards.WhiteKnights | bitboards.WhiteBishops | bitboards.WhiteRooks | bitboards.WhiteQueens | bitboards.WhiteKings
	occupancies[models.Black] = bitboards.BlackPawns | bitboards.BlackKnights | bitboards.BlackBishops | bitboards.BlackRooks | bitboards.BlackQueens | bitboards.BlackKings
	combinedOccupancy := occupancies[models.White] | occupancies[models.Black]

	utils := models.NewBitboardUtils()

	// Default to white's turn. Note: Ideally parsed from FEN or GameHistory state.
	sideToMove := models.White

	isValidMoveLocally := models.ValidateMove(bbMap, occupancies, combinedOccupancy, utils, sideToMove, msg.From, msg.To)
	log.Printf("[Game: %s] Local move validation result for %s -> %s: %v", gameID, msg.From, msg.To, isValidMoveLocally)

	if !isValidMoveLocally {
		log.Printf("[Game: %s] Warning: Move rejected by local validation logic.", gameID)
		// We can return a rejected payload here, but we will let it proceed to show integration for now.
	}

	predictedMoveUci, err := services.PredictMove(context.Background(), gameID, bitboards)
	if err != nil {
		log.Printf("Failed to get predicted move: %v", err)
	}

	// Create mock response
	resp := ws.MoveResponse{
		Type:    "move_validation",
		IsValid: true,
		Move:    predictedMoveUci, // e.g. "e2e4"
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
