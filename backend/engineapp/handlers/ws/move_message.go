package ws

type Side struct {
	Value string `json:"_value"`
}

type PieceType struct {
	Type string `json:"_type"`
}

type MovePiece struct {
	Side      Side      `json:"_side"`
	PieceType PieceType `json:"_type"`
}

// MoveMessage represents an incoming chess move payload
type MoveMessage struct {
	GameID        string    `json:"game_id"`
	CapturedPiece MovePiece `json:"capturedPiece"`
	Piece         MovePiece `json:"piece"`
	From          string    `json:"from"`
	To            string    `json:"to"`
}

type PieceMoved struct {
	GameID string    `json:"game_id"`
	From   string    `json:"from"`
	To     string    `json:"to"`
	Piece  MovePiece `json:"piece"`
}

type PieceMoveFailed struct {
	GameID    string    `json:"game_id"`
	From      string    `json:"from"`
	To        string    `json:"to"`
	Piece     MovePiece `json:"piece"`
	Reason    string    `json:"reason"`
	EventType string    `json:"event_type"`
}

type KingCastled struct {
	GameID   string `json:"game_id"`
	Side     Side   `json:"side"`
	KingFrom string `json:"king_from"`
	KingTo   string `json:"king_to"`
	RookFrom string `json:"rook_from"`
	RookTo   string `json:"rook_to"`
	KingSide bool   `json:"is_kingside"` // "true" or "false"
}

type PieceCaptured struct {
	GameID string    `json:"game_id"`
	From   string    `json:"from"`
	To     string    `json:"to"`
	Piece  MovePiece `json:"piece"`
}

type KingChecked struct {
	GameID   string `json:"game_id"`
	Side     Side   `json:"side"`
	Position string `json:"position"`
}

type KingCheckMated struct {
	GameID   string `json:"game_id"`
	Side     Side   `json:"side"`
	Position string `json:"position"`
}

type SyncedState struct {
	GameID     string   `json:"game_id"`
	Turn       Side     `json:"turn"`
	FEN        string   `json:"fen"`
	LegalMoves []string `json:"legal_moves"`
}

type AIPredictedMove struct {
	GameID          string `json:"game_id"`
	PredictedAiMove string `json:"predicted_ai_move"`
	EventType       string `json:"event_type"`
}
