package handlers

import (
	"encoding/json"
	"engineapp/database"
	"log"
	"net/http"
)

type GameHandler struct {
	Repo *database.MongoRepository
}

func NewGameHandler(repo *database.MongoRepository) *GameHandler {
	return &GameHandler{Repo: repo}
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
	game, err := h.Repo.GetGameState(r.Context(), gameID)
	log.Printf("Game: %v", game)
	if err != nil {
		log.Printf("Failed to fetch game by Id: %s", gameID)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to fetch game"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(game); err != nil {
		log.Printf("Failed to encode game JSON: %v", err)
	}
}

// RequestGame creates a new game state.
// @Summary Create game state
// @Description creates a new chess game state in the database
// @Tags games
// @Accept json
// @Produce json
// @Param game body database.GameState true "Game State"
// @Success 200 {object} database.GameState
// @Failure 400 {string} string "Failed to decode or create game"
// @Router /game [post]
func (h *GameHandler) RequestGame(w http.ResponseWriter, r *http.Request) {
	var game database.GameState
	if err := json.NewDecoder(r.Body).Decode(&game); err != nil {
		log.Printf("Failed to decode game JSON: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to decode game"))
		return
	}

	if err := h.Repo.CreateGameState(r.Context(), &game); err != nil {
		log.Printf("Failed to create game state: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to create game"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(game); err != nil {
		log.Printf("Failed to encode game JSON: %v", err)
	}
}
