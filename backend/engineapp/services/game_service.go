package services

import (
	"context"
	"engineapp/database"
	"engineapp/models"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type GameRepository interface {
	GetGame(ctx context.Context, gameID string) (*models.Game, error)
	CreateGameState(ctx context.Context, game *database.GameState) error
	CreateGameHistory(ctx context.Context, history *database.GameHistory) error
	CreateMatchingQueue(ctx context.Context, queueItem *database.MatchingQueue) error
	UpdateGameStatus(ctx context.Context, gameID string, status models.GameStatus, result string, reason string) error
}

type GameService interface {
	GetGame(ctx context.Context, gameID string) (*models.ChessGameDto, error)
	RequestComputerGame(ctx context.Context, userID string, req models.RequestComputerGame) (*models.ChessGameDto, error)
	RequestOnlineGame(ctx context.Context, userID string, req models.RequestOnlineGame) (*database.MatchingQueue, error)
}

type gameService struct {
	repo GameRepository
}

func NewGameService(repo GameRepository) GameService {
	return &gameService{repo: repo}
}

func (s *gameService) GetGame(ctx context.Context, gameID string) (*models.ChessGameDto, error) {
	game, err := s.repo.GetGame(ctx, gameID)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch game: %w", err)
	}
	if game == nil {
		return nil, nil // game not found
	}

	dto := mapGameToDto(game)
	return &dto, nil
}

func (s *gameService) RequestComputerGame(ctx context.Context, userID string, req models.RequestComputerGame) (*models.ChessGameDto, error) {
	gameFormat := models.NewGameFormat(req.Format, req.BaseTime, req.Increment)
	domainGame := models.NewComputerGame(userID, req.Color, gameFormat)

	dbGame := mapGameToDatabase(domainGame)

	if err := s.repo.CreateGameState(ctx, &dbGame); err != nil {
		return nil, fmt.Errorf("failed to create game state: %w", err)
	}

	startFen := req.StartingFEN
	if startFen == "" {
		startFen = models.FEN_START_POSITION
	}

	history := database.GameHistory{
		ID:         uuid.New().String(),
		GameID:     domainGame.ID(),
		OccurredAt: time.Now(),
		Sequence:   0,
		BoardFen:   startFen,
	}

	// create history so it can be loaded
	if err := s.repo.CreateGameHistory(ctx, &history); err != nil {
		return nil, fmt.Errorf("failed to create game history: %w", err)
	}

	loadedGame, err := s.repo.GetGame(ctx, domainGame.ID())
	if err != nil {
		return nil, fmt.Errorf("failed to get created game: %w", err)
	}
	if loadedGame == nil {
		return nil, fmt.Errorf("created game not found")
	}

	dto := mapGameToDto(loadedGame)
	return &dto, nil
}

func (s *gameService) RequestOnlineGame(ctx context.Context, userID string, req models.RequestOnlineGame) (*database.MatchingQueue, error) {
	if userID == "" {
		userID = uuid.New().String()
	}

	queueItem := database.MatchingQueue{
		ID:              uuid.New().String(),
		PlayerID:        userID,
		ProfileID:       "guest",
		GameFormat:      req.Format,
		BaseTime:        req.BaseTime,
		Increment:       req.Increment,
		ColorPreference: req.ColorPreference,
		Rated:           req.Rated,
		Culture:         req.Culture,
		OpponentID:      req.OpponentID,
		Region:          "unknown", // ToDo: resolve from request or IP?
		RD:              0,
		Ping:            0,
		Ranking:         1200,
		CreatedAt:       time.Now(),
		ExpiresAt:       time.Now().Add(5 * time.Minute),
		Status:          "open",
	}

	if err := s.repo.CreateMatchingQueue(ctx, &queueItem); err != nil {
		return nil, fmt.Errorf("failed to create matching queue: %w", err)
	}

	return &queueItem, nil
}
