package ws

type Side struct {
	Value string `json:"_value"`
}

type Piece struct {
	Side      Side   `json:"_side"`
	PieceType string `json:"_type"`
}

// GameRequest represents an incoming chess move payload
type GameRequest struct {
	GameID        string `json:"game_id"`
	CapturedPiece Piece  `json:"capturedPiece"`
	Piece         Piece  `json:"piece"`
	From          string `json:"from"`
	To            string `json:"to"`
}

type GameState struct {
	IsCheck     bool `json:"is_check"`
	IsCheckmate bool `json:"is_checkmate"`
	IsStalemate bool `json:"is_stalemate"`
	IsDraw      bool `json:"is_draw"`
}

type AIPredictedMove struct {
	GameID          string `json:"game_id"`
	PredictedAiMove string `json:"predicted_ai_move"`
	EventType       string `json:"event_type"`
}

type GameUpdate struct {
	EventType string         `json:"event_type"`
	Data      GameUpdateData `json:"data"`
}

type GameUpdateData struct {
	Fen      []byte `json:"fen"`
	LastMove string `json:"last_move"`
	State    uint8  `json:"state"`
}

type SyncedStateEvent struct {
	EventType  string `json:"event_type"`
	GameID     string `json:"game_id"`
	Turn       string `json:"turn"`
	LegalMoves string `json:"legal_moves"`
}

type PieceMoveFailedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Reason    string `json:"reason"`
	From      string `json:"from_"`
	To        string `json:"to"`
}

type KingCheckedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Side      string `json:"side"`
	Position  string `json:"position"`
}

type GameFinishedEvent struct {
	EventType    string `json:"event_type"`
	GameID       string `json:"game_id"`
	Result       string `json:"result"`
	FinishedDate string `json:"finished_date"`
}

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

type PieceMovedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	From      string `json:"from"`
	To        string `json:"to"`
}

type PieceCapturedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	From      string `json:"from"`
	To        string `json:"to"`
	Captured  string `json:"captured"`
}

type KingCheckmatedEvent struct {
	EventType string `json:"event_type"`
	GameID    string `json:"game_id"`
	Side      string `json:"side"`
	Position  string `json:"position"`
}
