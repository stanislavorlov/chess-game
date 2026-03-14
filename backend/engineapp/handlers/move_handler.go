package handlers

import (
	"encoding/json"
	"log"

	"engineapp/handlers/ws"
)

// HandleMove processes an incoming move message for a given game
func HandleMove(gameID string, message []byte) []byte {
	var msg ws.MoveMessage
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return nil
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	// TODO: Call engine/gRPC layer for real move validation

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
