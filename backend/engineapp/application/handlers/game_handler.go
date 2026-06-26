package handlers

import (
	"encoding/json"
	"engineapp/infrastructure/middleware"
	"engineapp/domain/models"
	"engineapp/application/services"
	"log"
	"net/http"
)

type GameHandler struct {
	Service services.GameService
}

func NewGameHandler(service services.GameService) *GameHandler {
	return &GameHandler{Service: service}
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

	dto, err := h.Service.GetGame(r.Context(), gameID)
	if err != nil {
		log.Printf("Failed to fetch game by Id: %s, error: %v", gameID, err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to fetch game"))
		return
	}

	if dto == nil {
		http.Error(w, "Game not found", http.StatusNotFound)
		return
	}

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

	userId := middleware.GetUserID(r.Context())

	dto, err := h.Service.RequestComputerGame(r.Context(), userId, gameRequest)
	if err != nil {
		log.Printf("Failed to create game state: %v", err)
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("Failed to create game"))
		return
	}

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

	userId := middleware.GetUserID(r.Context())

	queueItem, err := h.Service.RequestOnlineGame(r.Context(), userId, gameRequest)
	if err != nil {
		log.Printf("Failed to create matching queue: %v", err)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Failed to create matching queue"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	if err := json.NewEncoder(w).Encode(queueItem); err != nil {
		log.Printf("Failed to encode game JSON: %v", err)
	}
}
