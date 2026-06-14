package handlers

import (
	"context"
	"encoding/json"
	"log"
	"statsapp/database"
	"statsapp/models"
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

// HandleChessEvent is a sample callback function to process incoming messages
func HandleChessEvent(message []byte) {
	log.Printf("Received Kafka message on chess_events: %s", string(message))

	var event map[string]interface{}
	if err := json.Unmarshal(message, &event); err != nil {
		log.Printf("Error unmarshaling message: %v", err)
		return
	}

	if eventType, ok := event["event_type"].(string); ok && eventType == "game_finished" {
		log.Printf("Processing game_finished event: %v", event)

		if database.StatCollection != nil {
			resultStr, _ := event["result"].(string)
			lightPlayer, _ := event["light_player"].(string)
			darkPlayer, _ := event["dark_player"].(string)
			gameID, _ := event["game_id"].(string)

			stat := models.Stat{
				GameID:      gameID,
				Type:        "game_result",
				Value:       1.0,
				Timestamp:   primitive.NewDateTimeFromTime(time.Now()),
				Result:      resultStr,
				LightPlayer: lightPlayer,
				DarkPlayer:  darkPlayer,
			}

			_, err := database.StatCollection.InsertOne(context.Background(), stat)
			if err != nil {
				log.Printf("Error inserting game stat: %v", err)
			} else {
				log.Println("Successfully saved game_finished stat to DB.")
			}

			log.Println("Successfully saved game_finished stats to DB.")
		}
	}
}
