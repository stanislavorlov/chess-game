package models

import "strings"

type PieceType string

const (
	King   PieceType = "K"
	Queen  PieceType = "Q"
	Bishop PieceType = "B"
	Knight PieceType = "N"
	Rook   PieceType = "R"
	Pawn   PieceType = "P"
)

var AllPieceTypes = []PieceType{Pawn, Knight, Bishop, Rook, Queen, King}

type PieceKey struct {
	Side      Side
	PieceType PieceType
}

func (pt PieceType) Symbol(side Side) string {
	if side == White {
		return string(pt)
	}
	return strings.ToLower(string(pt))
}
