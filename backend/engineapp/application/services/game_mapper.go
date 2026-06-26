package services

import (
	"engineapp/infrastructure/database"
	"engineapp/domain/models"
	"strings"
	"time"
)

func mapGameToDto(game *models.Game) models.ChessGameDto {
	if game == nil {
		return models.ChessGameDto{}
	}

	var checkSide *string
	var checkPos *string
	if game.IsCheck() {
		side := string(game.Turn())
		checkSide = &side
		checkPos = game.CheckPosition()
	}

	return models.ChessGameDto{
		GameID:     game.ID(),
		MovesCount: game.FullmoveNumber,
		Date:       time.Now(),
		Name:       string(game.FormatName()),
		State: models.GameStateDto{
			Turn:          string(game.Turn()),
			Started:       game.Status() == models.Started,
			Finished:      game.Status() == models.Finished,
			CheckSide:     checkSide,
			CheckPosition: checkPos,
			LegalMoves:    strings.Join(game.LegalMoves(), ","),
		},
		GameFormat: models.GameFormatDto{
			Value:              string(game.FormatName()),
			WhiteRemainingTime: game.FormatMinutes() * 60,
			BlackRemainingTime: game.FormatMinutes() * 60,
			MoveIncrement:      game.FormatIncrement(),
		},
		Players: models.PlayersDto{
			WhiteID: game.LightPlayer().ID,
			BlackID: game.DarkPlayer().ID,
		},
		Board:   game.FEN(),
		History: game.History(),
	}
}

func mapGameToDatabase(domainGame *models.Game) database.GameState {
	return database.GameState{
		ID:        domainGame.ID(),
		Status:    string(domainGame.Status()),
		CreatedAt: time.Now(),
		StartedAt: time.Now(),
		Mode:      string(domainGame.Mode()),
		Format: database.GameFormat{
			Name:            domainGame.FormatName(),
			Minutes:         domainGame.FormatMinutes(),
			MoveIncrementMs: domainGame.FormatIncrement(),
		},
		Players: database.GamePlayers{
			LightPlayerId: domainGame.LightPlayer().ID,
			DarkPlayerId:  domainGame.DarkPlayer().ID,
		},
	}
}
