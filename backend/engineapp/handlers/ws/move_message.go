package ws

type Piece struct {
	Side      string `json:"_side"`
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
