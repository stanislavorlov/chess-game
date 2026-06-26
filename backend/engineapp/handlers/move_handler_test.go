package handlers

import (
	"context"
	"encoding/json"
	"strings"
	"testing"
	"time"

	"engineapp/database"
	"engineapp/factories"
	"engineapp/handlers/ws"
	"engineapp/models"
)

// MockGameRepo implements GameRepository for testing
type MockGameRepo struct {
	gameToReturn *models.Game
	errToReturn  error
	histories    []*database.GameHistory
	statuses     []string
}

func (m *MockGameRepo) GetGame(ctx context.Context, gameID string) (*models.Game, error) {
	return m.gameToReturn, m.errToReturn
}

func (m *MockGameRepo) CreateGameHistory(ctx context.Context, history *database.GameHistory) error {
	m.histories = append(m.histories, history)
	return nil
}

func (m *MockGameRepo) UpdateGameStatus(ctx context.Context, gameID string, status models.GameStatus, result string, reason string) error {
	m.statuses = append(m.statuses, string(status))
	return nil
}

// MockEventProducer implements EventProducer for testing
type MockEventProducer struct {
	produced []string
}

func (m *MockEventProducer) Produce(topic string, key []byte, value []byte) error {
	m.produced = append(m.produced, string(value))
	return nil
}

// MockAIPredictor implements AIPredictor for testing
type MockAIPredictor struct {
	predictedMove string
	errToReturn   error
	calls         int
}

func (m *MockAIPredictor) PredictMove(ctx context.Context, gameID string, bitboards models.Bitboards, isWhiteTurn bool) (string, error) {
	m.calls++
	return m.predictedMove, m.errToReturn
}

func createTestGame(fen string, mode models.GameMode) *models.Game {
	light := models.NewAuthenticatedPlayer("p1")
	dark := models.NewAuthenticatedPlayer("p2")
	if mode == models.ModeBot {
		dark = models.NewBotPlayer()
	}
	format := models.NewGameFormat("blitz", 3, 2)
	return factories.LoadGame("g1", models.Started, format, mode, light, dark, fen, nil, "")
}

func TestHandleMove_ValidMove(t *testing.T) {
	// Standard starting position
	game := createTestGame("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", models.ModeOnline)
	repo := &MockGameRepo{gameToReturn: game}
	producer := &MockEventProducer{}
	predictor := &MockAIPredictor{}

	handler := NewMoveHandler(repo, producer, predictor)

	req := ws.GameRequest{From: "e2", To: "e4"}
	reqBytes, _ := json.Marshal(req)

	var broadcasted []string
	send := func(b []byte) {}
	broadcast := func(b []byte) { broadcasted = append(broadcasted, string(b)) }

	handler.HandleMove("g1", reqBytes, send, broadcast)

	if len(repo.histories) != 1 {
		t.Errorf("Expected 1 history saved, got %d", len(repo.histories))
	}

	foundMoved := false
	foundSynced := false
	for _, b := range broadcasted {
		if strings.Contains(b, ws.EventPieceMoved) {
			foundMoved = true
		}
		if strings.Contains(b, ws.EventSyncedState) {
			foundSynced = true
		}
	}
	if !foundMoved {
		t.Errorf("Expected PieceMoved event")
	}
	if !foundSynced {
		t.Errorf("Expected SyncedState event")
	}
}

func TestHandleMove_InvalidMove(t *testing.T) {
	game := createTestGame("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", models.ModeOnline)
	repo := &MockGameRepo{gameToReturn: game}
	handler := NewMoveHandler(repo, &MockEventProducer{}, &MockAIPredictor{})

	// Illegal move: pawn e2 to e5
	req := ws.GameRequest{From: "e2", To: "e5"}
	reqBytes, _ := json.Marshal(req)

	var sent []string
	send := func(b []byte) { sent = append(sent, string(b)) }
	broadcast := func(b []byte) {}

	handler.HandleMove("g1", reqBytes, send, broadcast)

	if len(repo.histories) != 0 {
		t.Errorf("Expected 0 history saved for invalid move, got %d", len(repo.histories))
	}

	foundFailed := false
	for _, s := range sent {
		if strings.Contains(s, ws.EventPieceMoveFailed) {
			foundFailed = true
		}
	}
	if !foundFailed {
		t.Errorf("Expected PieceMoveFailed event")
	}
}

func TestHandleMove_CaptureMove(t *testing.T) {
	// e4 d5 setup, White to move pawn to d5
	game := createTestGame("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 2", models.ModeOnline)
	repo := &MockGameRepo{gameToReturn: game}
	handler := NewMoveHandler(repo, &MockEventProducer{}, &MockAIPredictor{})

	req := ws.GameRequest{From: "e4", To: "d5"}
	reqBytes, _ := json.Marshal(req)

	var broadcasted []string
	send := func(b []byte) {}
	broadcast := func(b []byte) { broadcasted = append(broadcasted, string(b)) }

	handler.HandleMove("g1", reqBytes, send, broadcast)

	foundCapture := false
	for _, b := range broadcasted {
		if strings.Contains(b, ws.EventPieceCaptured) {
			foundCapture = true
		}
	}
	if !foundCapture {
		t.Errorf("Expected PieceCaptured event")
	}
}

func TestHandleMove_Castling(t *testing.T) {
	// White ready to castle kingside
	game := createTestGame("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1", models.ModeOnline)
	repo := &MockGameRepo{gameToReturn: game}
	handler := NewMoveHandler(repo, &MockEventProducer{}, &MockAIPredictor{})

	req := ws.GameRequest{From: "e1", To: "g1"} // e1g1
	reqBytes, _ := json.Marshal(req)

	var broadcasted []string
	send := func(b []byte) {}
	broadcast := func(b []byte) { broadcasted = append(broadcasted, string(b)) }

	handler.HandleMove("g1", reqBytes, send, broadcast)

	foundCastle := false
	for _, b := range broadcasted {
		if strings.Contains(b, ws.EventKingCastled) {
			foundCastle = true
		}
	}
	if !foundCastle {
		t.Errorf("Expected KingCastled event")
	}
}

func TestHandleMove_Checkmate(t *testing.T) {
	// Fool's mate position, Black to deliver checkmate
	game := createTestGame("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2", models.ModeOnline)
	repo := &MockGameRepo{gameToReturn: game}
	producer := &MockEventProducer{}
	handler := NewMoveHandler(repo, producer, &MockAIPredictor{})

	req := ws.GameRequest{From: "d8", To: "h4"} // Qh4#
	reqBytes, _ := json.Marshal(req)

	var broadcasted []string
	send := func(b []byte) {}
	broadcast := func(b []byte) { broadcasted = append(broadcasted, string(b)) }

	handler.HandleMove("g1", reqBytes, send, broadcast)

	foundCheckmate := false
	foundFinished := false
	for _, b := range broadcasted {
		if strings.Contains(b, ws.EventKingCheckmated) {
			foundCheckmate = true
		}
		if strings.Contains(b, ws.EventGameFinished) {
			foundFinished = true
		}
	}
	if !foundCheckmate {
		t.Errorf("Expected KingCheckmated event")
	}
	if !foundFinished {
		t.Errorf("Expected GameFinished event")
	}

	if len(repo.statuses) != 1 || repo.statuses[0] != string(models.Finished) {
		t.Errorf("Expected game status to be updated to Finished")
	}

	// Should also produce Kafka event
	if len(producer.produced) == 0 || !strings.Contains(producer.produced[0], "game_finished") {
		t.Errorf("Expected game_finished kafka event")
	}
}

func TestHandleMove_BotModeTriggersAI(t *testing.T) {
	game := createTestGame("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", models.ModeBot)
	repo := &MockGameRepo{gameToReturn: game}
	predictor := &MockAIPredictor{predictedMove: "e7e5"}
	handler := NewMoveHandler(repo, &MockEventProducer{}, predictor)

	req := ws.GameRequest{From: "e2", To: "e4"}
	reqBytes, _ := json.Marshal(req)

	send := func(b []byte) {}
	broadcast := func(b []byte) {}

	handler.HandleMove("g1", reqBytes, send, broadcast)

	// Since AI prediction is triggered in a goroutine, we need to wait briefly
	time.Sleep(50 * time.Millisecond)

	if predictor.calls == 0 {
		t.Errorf("Expected AIPredictor to be called")
	}
}

func TestHandleConnect_InitialAI(t *testing.T) {
	// Game where history count will be exactly 1 (from our mock, but wait: history count is derived from game struct.
	game := factories.LoadGame("g1", models.Started, models.NewGameFormat("blitz", 3, 2), models.ModeBot, models.NewBotPlayer(), models.NewAuthenticatedPlayer("p2"), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", nil, "")
	repo := &MockGameRepo{gameToReturn: game}
	predictor := &MockAIPredictor{predictedMove: "e2e4"}
	handler := NewMoveHandler(repo, &MockEventProducer{}, predictor)

	send := func(b []byte) {}
	broadcast := func(b []byte) {}

	handler.HandleConnect("g1", send, broadcast)

	time.Sleep(50 * time.Millisecond)

	if predictor.calls == 0 {
		t.Errorf("Expected AIPredictor to be called on connect for Bot as White")
	}
}
