package models

const (
	EventAIPredictedMove = "ai-predicted-move"
	EventSyncedState     = "synced-state"
	EventPieceMoveFailed = "piece-move-failed"
	EventKingChecked     = "king-checked"
	EventGameFinished    = "game-finished"
	EventKingCastled     = "king-castled"
	EventPieceMoved      = "piece-moved"
	EventPieceCaptured   = "piece-captured"
	EventKingCheckmated  = "king-checkmated"
)

type DomainEvent interface {
	EventName() string
	ShouldBroadcast() bool
}

type AIPredictedMove struct {
	GameID          string `json:"game_id"`
	PredictedAiMove string `json:"predicted_ai_move"`
	EventType       string `json:"event_type"`
}
func (e AIPredictedMove) EventName() string { return e.EventType }
func (e AIPredictedMove) ShouldBroadcast() bool { return true }

type SyncedStateEvent struct {
	EventType  string `json:"event_type"`
	GameID     string `json:"game_id"`
	Turn       string `json:"turn"`
	LegalMoves string `json:"legal_moves"`
}
func (e SyncedStateEvent) EventName() string { return e.EventType }
func (e SyncedStateEvent) ShouldBroadcast() bool { return true }

type PieceMoveFailedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Reason    string `json:"reason"`
	From      string `json:"from_"`
	To        string `json:"to"`
}
func (e PieceMoveFailedEvent) EventName() string { return e.EventType }
func (e PieceMoveFailedEvent) ShouldBroadcast() bool { return false } // Send only to actor

type KingCheckedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Side      string `json:"side"`
	Position  string `json:"position"`
}
func (e KingCheckedEvent) EventName() string { return e.EventType }
func (e KingCheckedEvent) ShouldBroadcast() bool { return true }

type GameFinishedEvent struct {
	EventType    string `json:"event_type"`
	GameID       string `json:"game_id"`
	Result       string `json:"result"`
	FinishedDate string `json:"finished_date"`
}
func (e GameFinishedEvent) EventName() string { return e.EventType }
func (e GameFinishedEvent) ShouldBroadcast() bool { return true }

type KingCastledEvent struct {
	EventType  string `json:"event_type"`
	GameID     string `json:"game_id"`
	Side       string `json:"side"`
	KingFrom   string `json:"king_from"`
	KingTo     string `json:"king_to"`
	RookFrom   string `json:"rook_from"`
	RookTo     string `json:"rook_to"`
	IsKingside bool   `json:"is_kingside"`
}
func (e KingCastledEvent) EventName() string { return e.EventType }
func (e KingCastledEvent) ShouldBroadcast() bool { return true }

type PieceMovedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	From      string `json:"from"`
	To        string `json:"to"`
}
func (e PieceMovedEvent) EventName() string { return e.EventType }
func (e PieceMovedEvent) ShouldBroadcast() bool { return true }

type PieceCapturedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	From      string `json:"from"`
	To        string `json:"to"`
	Captured  string `json:"captured"`
}
func (e PieceCapturedEvent) EventName() string { return e.EventType }
func (e PieceCapturedEvent) ShouldBroadcast() bool { return true }

type KingCheckmatedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Side      string `json:"side"`
	Position  string `json:"position"`
}
func (e KingCheckmatedEvent) EventName() string { return e.EventType }
func (e KingCheckmatedEvent) ShouldBroadcast() bool { return true }
