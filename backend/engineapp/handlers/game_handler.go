package handlers

import (
	"encoding/json"
	"engineapp/database"
	"engineapp/models"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/google/uuid"
)

type GameHandler struct {
	Repo *database.MongoRepository
}

func NewGameHandler(repo *database.MongoRepository) *GameHandler {
	return &GameHandler{Repo: repo}
}

func GetIpAddress(r *http.Request) string {
	ip := r.Header.Get("X-Forwarded-For")
	if ip == "" {
		ip = r.RemoteAddr
	}
	return ip
}

func mapGameToDto(game *models.Game) models.ChessGameDto {
	if game == nil {
		return models.ChessGameDto{}
	}

	var checkSide *string
	var checkPos *string
	if game.IsCheck() {
		side := game.Turn()
		checkSide = &side
		checkPos = game.CheckPosition()
	}

	return models.ChessGameDto{
		GameID:     game.ID(),
		MovesCount: game.FullmoveNumber,
		Date:       time.Now(),
		Name:       string(game.FormatName()),
		State: models.GameStateDto{
			Turn:          game.Turn(),
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
			WhiteID: "computer",
			BlackID: "computer",
		},
		Board:   game.FEN(),
		History: game.History(),
	}
}

// GetGame retrieves a game state by its ID.
// @Summary Get game state
// @Description retrieves the current state of a chess game from the database
// @Tags games
// @Param gameId path string true "Game ID"
// @Produce plain
// @Success 200 {string} string "Game status"
// @Failure 400 {string} string "gameId is required or failed to fetch game"
// @Router /game/{gameId} [get]
func (h *GameHandler) GetGame(w http.ResponseWriter, r *http.Request) {
	gameID := r.PathValue("gameId")
	if gameID == "" {
		http.Error(w, "gameId is required", http.StatusBadRequest)
		return
	}
	game, err := h.Repo.GetGame(r.Context(), gameID)
	log.Printf("Game: %v", game)
	if err != nil {
		log.Printf("Failed to fetch game by Id: %s", gameID)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to fetch game"))
		return
	}

	if game == nil {
		http.Error(w, "Game not found", http.StatusNotFound)
		return
	}

	dto := mapGameToDto(game)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(dto); err != nil {
		log.Printf("Failed to encode game JSON: %v", err)
	}
}

// RequestComputerGame creates a new computer game state.
// @Summary Create computer game state
// @Description creates a new chess game state in the database
// @Tags games
// @Accept json
// @Produce json
// @Param game body models.RequestComputerGame true "Game State"
// @Success 200 {object} database.GameState
// @Failure 400 {string} string "Failed to decode or create game"
// @Router /game/computer [post]
func (h *GameHandler) RequestComputerGame(w http.ResponseWriter, r *http.Request) {
	var gameRequest models.RequestComputerGame
	if err := json.NewDecoder(r.Body).Decode(&gameRequest); err != nil {
		log.Printf("Failed to decode game JSON: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to decode game"))
		return
	}

	gameId := uuid.New().String()

	lightPlayer := "guest"
	darkPlayer := "computer"

	color := strings.ToLower(gameRequest.Color)
	if color == "random" {
		if time.Now().UnixNano()%2 == 0 {
			color = "black"
		} else {
			color = "white"
		}
	}

	if color == "black" {
		lightPlayer = "computer"
		darkPlayer = "guest"
	}

	game := database.GameState{
		ID:         gameId,
		Status:     "started",
		CreatedAt:  time.Now(),
		StartedAt:  time.Now(),
		Mode:       "bot",
		Format: database.GameFormat{
			Name:            gameRequest.Format,
			Minutes:         gameRequest.BaseTime,
			MoveIncrementMs: gameRequest.Increment,
		},
		Players: database.GamePlayers{
			LightPlayerId: lightPlayer,
			DarkPlayerId:  darkPlayer,
		},
	}

	if err := h.Repo.CreateGameState(r.Context(), &game); err != nil {
		log.Printf("Failed to create game state: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to create game"))
		return
	}

	startFen := gameRequest.StartingFEN
	if startFen == "" {
		startFen = models.FEN_START_POSITION
	}

	history := database.GameHistory{
		ID:         uuid.New().String(),
		GameID:     gameId,
		OccurredAt: time.Now(),
		Sequence:   0,
		BoardFen:   startFen,
	}

	// create history so it can be loaded
	if err := h.Repo.CreateGameHistory(r.Context(), &history); err != nil {
		log.Printf("Failed to create game history: %v", err)
	}

	loadedGame, _ := h.Repo.GetGame(r.Context(), gameId)
	dto := mapGameToDto(loadedGame)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(dto); err != nil {
		log.Printf("Failed to encode game JSON: %v", err)
	}
}

// RequestOnlineGame creates a new online game state.
// @Summary Create a record in the Matching queue
// @Description requests a new online game
// @Tags games
// @Accept json
// @Produce json
// @Param game body models.RequestOnlineGame true "Game State"
// @Success 200 {object} database.GameState
// @Failure 400 {string} string "Failed to decode or create game"
// @Router /game/online [post]
func (h *GameHandler) RequestOnlineGame(w http.ResponseWriter, r *http.Request) {
	var gameRequest models.RequestOnlineGame
	if err := json.NewDecoder(r.Body).Decode(&gameRequest); err != nil {
		log.Printf("Failed to decode game JSON: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to decode game"))
		return
	}

	queueItem := database.MatchingQueue{
		ID:              uuid.New().String(),
		PlayerID:        "guest", // ToDo: Get from auth context
		ProfileID:       "guest",
		GameFormat:      gameRequest.Format,
		BaseTime:        gameRequest.BaseTime,
		Increment:       gameRequest.Increment,
		ColorPreference: gameRequest.ColorPreference,
		Rated:           gameRequest.Rated,
		Culture:         gameRequest.Culture,
		OpponentID:      gameRequest.OpponentID,
		Region:          "unknown", // ToDo: resolve from request
		RD:              0,
		Ping:            0,
		Ranking:         1200,
		CreatedAt:       time.Now(),
		ExpiresAt:       time.Now().Add(5 * time.Minute),
		Status:          "open",
	}

	if err := h.Repo.CreateMatchingQueue(r.Context(), &queueItem); err != nil {
		log.Printf("Failed to create matching queue: %v", err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Failed to create matching queue"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(queueItem)
}
