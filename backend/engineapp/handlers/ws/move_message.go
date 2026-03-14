package ws

// MoveMessage represents an incoming chess move payload
type MoveMessage struct {
	GameID        string `json:"gameId"`
	CapturedPiece any    `json:"capturedPiece"`
	Piece         any    `json:"piece"`
	From          string `json:"from"`
	To            string `json:"to"`
}

// MoveResponse represents the result of validating a move
type MoveResponse struct {
	Type    string `json:"type"`
	IsValid bool   `json:"isValid"`
	Move    string `json:"move"`
	From    string `json:"from"`
	To      string `json:"to"`
}
