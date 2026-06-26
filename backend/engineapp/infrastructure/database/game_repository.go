package database

import (
	"context"
	"engineapp/domain/models"
)

// GameRepository defines the database operations required by the MoveHandler.
type GameRepository interface {
	GetGame(ctx context.Context, gameID string) (*models.Game, error)
	CreateGameHistory(ctx context.Context, history *GameHistory) error
	UpdateGameStatus(ctx context.Context, gameID string, status models.GameStatus, result string, reason string) error
}
