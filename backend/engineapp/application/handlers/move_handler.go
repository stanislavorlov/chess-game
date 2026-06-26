package handlers

import (
	"context"
	"encoding/json"
	"log"

	"engineapp/infrastructure/database"
	"engineapp/application/handlers/ws"
	"engineapp/application/ports"
	"engineapp/domain/models"
)

// MoveHandler manages move-related requests and their dependencies.
type MoveHandler struct {
	Repo      database.GameRepository
	Producer  ports.EventProducer
	Predictor ports.AIPredictor
}

// NewMoveHandler creates a new MoveHandler instance.
func NewMoveHandler(repo database.GameRepository, producer ports.EventProducer, predictor ports.AIPredictor) *MoveHandler {
	return &MoveHandler{Repo: repo, Producer: producer, Predictor: predictor}
}

// HandleMove processes an incoming move message for a given game
func (h *MoveHandler) HandleMove(gameID string, message []byte, send func([]byte), broadcast func([]byte)) {
	var msg ws.GameRequest
	if err := json.Unmarshal(message, &msg); err != nil {
		log.Printf("Error parsing move JSON: %v", err)
		return
	}

	log.Printf("[Game: %s] Parsed move: %+v", gameID, msg)

	game, err := h.Repo.GetGame(context.Background(), gameID)
	if err != nil {
		log.Printf("[Game: %s] Failed to get Game: %v", gameID, err)
		return
	}

	pieceStr := msg.Piece.Side.Value + msg.Piece.PieceType
	game.MovePiece(msg.From, msg.To, pieceStr)

	events, success := game.PopEvents()

	if success {
		err = h.Repo.CreateGameHistory(context.Background(), &database.GameHistory{
			GameID:  gameID,
			SanMove: msg.From + msg.To,
		})
		if err != nil {
			log.Printf("Failed to create game history: %v", err)
		}
	}

	for _, event := range events {
		eventBytes, _ := json.Marshal(event)
		if event.ShouldBroadcast() {
			broadcast(eventBytes)
		} else {
			send(eventBytes)
		}

		if event.EventName() == models.EventGameFinished {
			h.Producer.Produce("games", []byte(gameID), eventBytes)
			h.Repo.UpdateGameStatus(context.Background(), gameID, game.Status(), game.Result(), "Domain Event")
		}
	}

	if game.Mode() == models.ModeBot {
		isWhiteTurn := game.Turn() == models.White
		isBotTurn := (isWhiteTurn && game.LightPlayer() != nil && game.LightPlayer().IsBot) || (!isWhiteTurn && game.DarkPlayer() != nil && game.DarkPlayer().IsBot)

		if isBotTurn {
			// 2. Asynchronously request AI prediction and publish it
			go func() {
				predictedMoveUci, err := h.Predictor.PredictMove(context.Background(), gameID, game.Bitboards, isWhiteTurn)
				if err != nil {
					log.Printf("Failed to get predicted move: %v", err)
					return
				}

				// Publish AI move prediction
				resp2Bytes, _ := json.Marshal(models.AIPredictedMove{
					GameID:          gameID,
					PredictedAiMove: predictedMoveUci,
					EventType:       models.EventAIPredictedMove,
				})
				broadcast(resp2Bytes)
			}()
		}
	}
}

// HandleConnect triggers initial actions when a client connects to the WebSocket
func (h *MoveHandler) HandleConnect(gameID string, send func([]byte), broadcast func([]byte)) {
	game, err := h.Repo.GetGame(context.Background(), gameID)
	if err != nil || game == nil {
		return
	}

	// Only trigger if no moves have been played yet (history count == 1, which is the initial state)
	if game.HistoryCount() > 1 {
		return
	}

	if game.Mode() == models.ModeBot {
		isWhiteTurn := game.Turn() == models.White
		isBotTurn := (isWhiteTurn && game.LightPlayer() != nil && game.LightPlayer().IsBot) || (!isWhiteTurn && game.DarkPlayer() != nil && game.DarkPlayer().IsBot)

		if isBotTurn {
			log.Printf("[Game: %s] Triggering initial AI prediction on connect", gameID)
			go func() {
				predictedMoveUci, err := h.Predictor.PredictMove(context.Background(), gameID, game.Bitboards, isWhiteTurn)
				if err != nil {
					log.Printf("Failed to get initial predicted move: %v", err)
					return
				}

				respBytes, _ := json.Marshal(models.AIPredictedMove{
					GameID:          gameID,
					PredictedAiMove: predictedMoveUci,
					EventType:       models.EventAIPredictedMove,
				})
				broadcast(respBytes)
			}()
		}
	}
}
