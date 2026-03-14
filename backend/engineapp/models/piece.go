package models

type PieceType string

const (
	King   PieceType = "K"
	Queen  PieceType = "Q"
	Bishop PieceType = "B"
	Knight PieceType = "N"
	Rook   PieceType = "R"
	Pawn   PieceType = "P"
)

type PieceKey struct {
	Side      Side
	PieceType PieceType
}
