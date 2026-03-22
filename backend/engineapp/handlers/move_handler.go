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
func (h *MoveHandler) HandleMove(gameID string, message []byte) []byte {
	var msg ws.MoveMessage
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return nil
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	// Restore game state from Redis or FastAPI gRPC
	/*boardState, err := services.GetGameState(context.Background(), gameID)
	if err != nil {
		log.Printf("[Game: %s] Failed to get GameState: %v", gameID, err)
	} else {
		log.Printf("[Game: %s] Restored Board State FEN: %s", gameID, boardState.Fen)
	}

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
	}*/

	// ToDo: move all the Database & Mongo logic to the Go engine app

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

	predictedMoveUci, err := services.PredictMove(context.Background(), gameID, latestEntry)
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
