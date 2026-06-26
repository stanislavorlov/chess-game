package models

type Bitboards struct {
	WhitePawns   uint64
	WhiteKnights uint64
	WhiteBishops uint64
	WhiteRooks   uint64
	WhiteQueens  uint64
	WhiteKings   uint64
	BlackPawns   uint64
	BlackKnights uint64
	BlackBishops uint64
	BlackRooks   uint64
	BlackQueens  uint64
	BlackKings   uint64
}

// GenerateMaps transforms the discrete bitboard fields into a piece map and occupancy bitboards.
func (b *Bitboards) GenerateMaps() (map[PieceKey]uint64, map[Side]uint64, uint64) {
	bbMap := make(map[PieceKey]uint64)
	bbMap[PieceKey{Side: White, PieceType: Pawn}] = b.WhitePawns
	bbMap[PieceKey{Side: White, PieceType: Knight}] = b.WhiteKnights
	bbMap[PieceKey{Side: White, PieceType: Bishop}] = b.WhiteBishops
	bbMap[PieceKey{Side: White, PieceType: Rook}] = b.WhiteRooks
	bbMap[PieceKey{Side: White, PieceType: Queen}] = b.WhiteQueens
	bbMap[PieceKey{Side: White, PieceType: King}] = b.WhiteKings

	bbMap[PieceKey{Side: Black, PieceType: Pawn}] = b.BlackPawns
	bbMap[PieceKey{Side: Black, PieceType: Knight}] = b.BlackKnights
	bbMap[PieceKey{Side: Black, PieceType: Bishop}] = b.BlackBishops
	bbMap[PieceKey{Side: Black, PieceType: Rook}] = b.BlackRooks
	bbMap[PieceKey{Side: Black, PieceType: Queen}] = b.BlackQueens
	bbMap[PieceKey{Side: Black, PieceType: King}] = b.BlackKings

	occupancies := make(map[Side]uint64)
	occupancies[White] = b.WhitePawns | b.WhiteKnights | b.WhiteBishops | b.WhiteRooks | b.WhiteQueens | b.WhiteKings
	occupancies[Black] = b.BlackPawns | b.BlackKnights | b.BlackBishops | b.BlackRooks | b.BlackQueens | b.BlackKings
	
	combinedOccupancy := occupancies[White] | occupancies[Black]

	return bbMap, occupancies, combinedOccupancy
}
