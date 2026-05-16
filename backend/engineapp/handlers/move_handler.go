package handlers

import (
	"context"
	"encoding/json"
	"log"
	"strings"
	"time"

	"github.com/google/uuid"

	"engineapp/database"
	"engineapp/handlers/ws"
	"engineapp/models"
	"engineapp/services"
)

// MoveHandler manages move-related requests and their dependencies.
type MoveHandler struct {
	Repo *database.MongoRepository
}

// NewMoveHandler creates a new MoveHandler instance.
func NewMoveHandler(repo *database.MongoRepository) *MoveHandler {
	return &MoveHandler{Repo: repo}
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

	movePieceResult := game.MovePiece(msg)
	log.Printf("[Game: %s] Local move validation result for %s -> %s: %v (Castling: %v)", gameID, msg.From, msg.To, movePieceResult.Valid, movePieceResult.IsCastling)

	if !movePieceResult.Valid {
		log.Printf("[Game: %s] Warning: Move rejected by local validation logic.", gameID)

		failedEvent := ws.PieceMoveFailedEvent{
			EventType: ws.EventPieceMoveFailed,
			GameID:    gameID,
			Reason:    movePieceResult.Error,
			From:      msg.From,
			To:        msg.To,
		}

		if responseBytes, err := json.Marshal(failedEvent); err == nil {
			send(responseBytes)
		} else {
			log.Printf("Error marshaling move response: %v", err)
		}
		return
	}

	// Save the move to history
	historyEntry := database.GameHistory{
		ID:         uuid.New().String(),
		GameID:     gameID,
		OccurredAt: time.Now(),
		Sequence:   game.HistoryCount(),
		BoardFen:   game.FEN(),
		SanMove:    msg.From + msg.To,
	}
	if err := h.Repo.CreateGameHistory(context.Background(), &historyEntry); err != nil {
		log.Printf("[Game: %s] Failed to save move to history: %v", gameID, err)
	}

	if movePieceResult.IsCastling {
		castledEvent := ws.KingCastledEvent{
			EventType:  ws.EventKingCastled,
			GameID:     gameID,
			Side:       string(game.Turn()), // This is the side that just moved (wait, no, game.Turn() was toggled)
			KingFrom:   msg.From,
			KingTo:     msg.To,
			RookFrom:   string(movePieceResult.CastlingRookFrom),
			RookTo:     string(movePieceResult.CastlingRookTo),
			IsKingside: movePieceResult.IsKingside,
		}
		// The side in the event should be the side that DID the castling.
		// Since MovePiece toggled the turn, we need the OPPOSITE side.
		if game.Turn() == models.White {
			castledEvent.Side = string(models.Black)
		} else {
			castledEvent.Side = string(models.White)
		}

		if respBytes, err := json.Marshal(castledEvent); err == nil {
			broadcast(respBytes)
		}
	} else if movePieceResult.IsCapture {
		capturedEvent := ws.PieceCapturedEvent{
			EventType: ws.EventPieceCaptured,
			GameID:    gameID,
			From:      msg.From,
			To:        msg.To,
			Captured:  movePieceResult.CapturedPiece,
		}
		if respBytes, err := json.Marshal(capturedEvent); err == nil {
			broadcast(respBytes)
		}
	} else {
		movedEvent := ws.PieceMovedEvent{
			EventType: ws.EventPieceMoved,
			GameID:    gameID,
			From:      msg.From,
			To:        msg.To,
		}
		if respBytes, err := json.Marshal(movedEvent); err == nil {
			broadcast(respBytes)
		}
	}

	syncedEvent := ws.SyncedStateEvent{
		EventType:  ws.EventSyncedState,
		GameID:     gameID,
		Turn:       string(game.Turn()),
		LegalMoves: strings.Join(game.LegalMoves(), ","),
	}
	resp1Bytes, _ := json.Marshal(syncedEvent)
	broadcast(resp1Bytes)

	if game.IsCheck() {
		pos := game.CheckPosition()
		if pos != nil {
			checkEvent := ws.KingCheckedEvent{
				EventType: ws.EventKingChecked,
				GameID:    gameID,
				Side:      string(game.Turn()),
				Position:  *pos,
			}
			if respBytes, err := json.Marshal(checkEvent); err == nil {
				broadcast(respBytes)
			}
		}
	}

	if game.IsCheckmate() {
		game.FinishGame()
		winner := string(models.SideNameBlack)
		if game.Turn() == models.Black {
			winner = string(models.SideNameWhite)
		}
		game.SetResult(winner + " wins by checkmate")

		pos := game.CheckPosition()
		if pos != nil {
			checkmatedEvent := ws.KingCheckmatedEvent{
				EventType: ws.EventKingCheckmated,
				GameID:    gameID,
				Side:      string(game.Turn()),
				Position:  *pos,
			}
			if respBytes, err := json.Marshal(checkmatedEvent); err == nil {
				broadcast(respBytes)
			}
		}
	} else if game.IsStalemate() {
		game.FinishGame()
		game.SetResult("Draw by stalemate")
	}

	if game.Status() == models.Finished {
		if err := h.Repo.UpdateGameStatus(context.Background(), gameID, game.Status(), game.Result()); err != nil {
			log.Printf("[Game: %s] Failed to update game status in repo: %v", gameID, err)
		}

		finishedEvent := ws.GameFinishedEvent{
			EventType:    ws.EventGameFinished,
			GameID:       gameID,
			Result:       game.Result(),
			FinishedDate: time.Now().Format(time.RFC3339),
		}
		if respBytes, err := json.Marshal(finishedEvent); err == nil {
			broadcast(respBytes)
		}
	}

	if game.Mode() == models.ModeBot {
		isWhiteTurn := game.Turn() == models.White
		isBotTurn := (isWhiteTurn && game.LightPlayer() == models.PlayerComputer) || (!isWhiteTurn && game.DarkPlayer() == models.PlayerComputer)

		if isBotTurn {
			// 2. Asynchronously request AI prediction and publish it
			go func() {
				predictedMoveUci, err := services.PredictMove(context.Background(), gameID, game.Bitboards, isWhiteTurn)
				if err != nil {
					log.Printf("Failed to get predicted move: %v", err)
					return
				}

				// Publish AI move prediction
				resp2Bytes, _ := json.Marshal(ws.AIPredictedMove{
					GameID:          gameID,
					PredictedAiMove: predictedMoveUci,
					EventType:       ws.EventAIPredictedMove,
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
		isBotTurn := (isWhiteTurn && game.LightPlayer() == models.PlayerComputer) || (!isWhiteTurn && game.DarkPlayer() == models.PlayerComputer)

		if isBotTurn {
			log.Printf("[Game: %s] Triggering initial AI prediction on connect", gameID)
			go func() {
				predictedMoveUci, err := services.PredictMove(context.Background(), gameID, game.Bitboards, isWhiteTurn)
				if err != nil {
					log.Printf("Failed to get initial predicted move: %v", err)
					return
				}

				respBytes, _ := json.Marshal(ws.AIPredictedMove{
					GameID:          gameID,
					PredictedAiMove: predictedMoveUci,
					EventType:       ws.EventAIPredictedMove,
				})
				broadcast(respBytes)
			}()
		}
	}
}
