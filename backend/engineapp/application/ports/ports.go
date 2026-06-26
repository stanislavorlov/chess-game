package ports

import (
	"context"

	"engineapp/domain/models"
)

// EventProducer defines the message broker operations required by the Application.
type EventProducer interface {
	Produce(topic string, key []byte, value []byte) error
}

// AIPredictor defines the AI move prediction operations required by the Application.
type AIPredictor interface {
	PredictMove(ctx context.Context, gameID string, bitboards models.Bitboards, isWhiteTurn bool) (string, error)
}
