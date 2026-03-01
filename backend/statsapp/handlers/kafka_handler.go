package handlers

import (
	"log"
)

// HandleChessEvent is a sample callback function to process incoming messages
func HandleChessEvent(message []byte) {
	// Let's pretend the message is a JSON string from Python
	log.Printf("Received Kafka message on chess_events: %s", string(message))

	// In the real world, you might unmarshal the JSON here
	// var event map[string]interface{}
	// if err := json.Unmarshal(message, &event); err != nil {
	// 	log.Printf("Error unmarshaling message: %v", err)
	// }
}
