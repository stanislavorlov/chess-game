package models

import (
	"testing"
)

func TestSafeShift(t *testing.T) {
	if got := SafeShift(1, 1); got != 2 {
		t.Errorf("SafeShift(1, 1) = %d; want 2", got)
	}
	if got := SafeShift(2, -1); got != 1 {
		t.Errorf("SafeShift(2, -1) = %d; want 1", got)
	}
	if got := SafeShift(1, 64); got != 0 {
		t.Errorf("SafeShift(1, 64) = %d; want 0", got)
	}
	if got := SafeShift(1, -64); got != 0 {
		t.Errorf("SafeShift(1, -64) = %d; want 0", got)
	}
}

func TestBitOperations(t *testing.T) {
	var b uint64 = 0

	b = SetBit(b, 0)
	if !GetBit(b, 0) {
		t.Errorf("GetBit(b, 0) should be true after SetBit")
	}

	b = SetBit(b, 63)
	if !GetBit(b, 63) {
		t.Errorf("GetBit(b, 63) should be true after SetBit")
	}

	if count := CountBits(b); count != 2 {
		t.Errorf("CountBits(b) = %d; want 2", count)
	}

	b = ClearBit(b, 0)
	if GetBit(b, 0) {
		t.Errorf("GetBit(b, 0) should be false after ClearBit")
	}
}

func TestGetRookAttacks(t *testing.T) {
	// Empty board, rook at A1 (0) -> 14 attacks (7 rank, 7 file)
	attacks := GetRookAttacks(0, 0)
	if CountBits(attacks) != 14 {
		t.Errorf("Rook on A1 empty board attacks = %d; want 14", CountBits(attacks))
	}

	// Rook at A1, blocked at B1 (1) and A2 (8)
	occupancy := (1 << 1) | (1 << 8)
	attacks = GetRookAttacks(0, uint64(occupancy))
	if CountBits(attacks) != 2 {
		t.Errorf("Rook on A1 blocked at B1, A2 attacks = %d; want 2", CountBits(attacks))
	}
}

func TestGetBishopAttacks(t *testing.T) {
	// Empty board, bishop at D4 (27)
	attacks := GetBishopAttacks(27, 0)
	if CountBits(attacks) != 13 {
		t.Errorf("Bishop on D4 empty board attacks = %d; want 13", CountBits(attacks))
	}

	// Blocked at E5 (36), C5 (34), C3 (18), E3 (20)
	occupancy := (uint64(1) << 36) | (uint64(1) << 34) | (uint64(1) << 18) | (uint64(1) << 20)
	attacks = GetBishopAttacks(27, occupancy)
	if CountBits(attacks) != 4 {
		t.Errorf("Bishop tightly blocked attacks = %d; want 4", CountBits(attacks))
	}
}

func TestNewBitboardUtils(t *testing.T) {
	utils := NewBitboardUtils()
	if utils == nil {
		t.Fatal("NewBitboardUtils returned nil")
	}
	if utils.FileA != 0x0101010101010101 {
		t.Errorf("FileA mask incorrect")
	}
	if utils.Rank1 != 0x00000000000000FF {
		t.Errorf("Rank1 mask incorrect")
	}
	
	// Check Knight Moves for A1 (index 0)
	if CountBits(utils.KnightMoves[0]) != 2 {
		t.Errorf("Knight on A1 should have 2 moves, got %d", CountBits(utils.KnightMoves[0]))
	}

	// Check King Moves for A1 (index 0)
	if CountBits(utils.KingMoves[0]) != 3 {
		t.Errorf("King on A1 should have 3 moves, got %d", CountBits(utils.KingMoves[0]))
	}
}

func TestPositionConversions(t *testing.T) {
	pos := Position{File: FileA, Rank: Rank1}
	idx := ToBitIndex(pos)
	if idx != 0 {
		t.Errorf("ToBitIndex(A1) = %d; want 0", idx)
	}

	pos2 := BitIndexToPosition(0)
	if pos2.File != FileA || pos2.Rank != Rank1 {
		t.Errorf("BitIndexToPosition(0) = %+v; want A1", pos2)
	}

	posH8 := Position{File: FileH, Rank: Rank8}
	idxH8 := ToBitIndex(posH8)
	if idxH8 != 63 {
		t.Errorf("ToBitIndex(H8) = %d; want 63", idxH8)
	}

	pos2H8 := BitIndexToPosition(63)
	if pos2H8.File != FileH || pos2H8.Rank != Rank8 {
		t.Errorf("BitIndexToPosition(63) = %+v; want H8", pos2H8)
	}
}

func TestPawnMoves(t *testing.T) {
	utils := NewBitboardUtils()
	// White pawn at A2 (index 8)
	pawns := uint64(1 << 8)
	var combined uint64 = pawns
	var opponent uint64 = 0

	moves := GetPawnMoves(White, pawns, combined, opponent, utils, "-")
	if len(moves) != 2 {
		t.Errorf("White pawn at A2 should have 2 moves, got %d", len(moves))
	}

	// Opponent at B3 (index 17) -> capture right
	opponent = (1 << 17)
	combined |= opponent
	moves = GetPawnMoves(White, pawns, combined, opponent, utils, "-")
	if len(moves) != 3 {
		t.Errorf("White pawn at A2 with opponent at B3 should have 3 moves, got %d", len(moves))
	}
}

func TestGetSlidingMoves(t *testing.T) {
	utils := NewBitboardUtils() // Just to make sure logic exists
	_ = utils

	// Rook at A1 (0) with own occupancy at A2 (8) and block at B1 (1)
	pieces := uint64(1 << 0)
	ownOccupancy := uint64(1 << 8) | uint64(1 << 1)
	fullOccupancy := ownOccupancy

	moves := GetSlidingMoves(Rook, pieces, fullOccupancy, ownOccupancy)
	if len(moves) != 0 {
		t.Errorf("Rook blocked by own pieces should have 0 moves, got %d", len(moves))
	}
}

func TestIsSquareAttacked(t *testing.T) {
	utils := NewBitboardUtils()
	
	bitboards := make(map[PieceKey]uint64)
	// Black pawn at B3 (17) attacking A2 (8)
	bitboards[PieceKey{Side: Black, PieceType: Pawn}] = (1 << 17)
	
	attacked := IsSquareAttacked(8, Black, bitboards, (1<<17), utils)
	if !attacked {
		t.Errorf("A2 should be attacked by Black Pawn on B3")
	}

	// Black Rook on A8 (56) attacking A2 (8)
	bitboards[PieceKey{Side: Black, PieceType: Rook}] = (1 << 56)
	attackedRook := IsSquareAttacked(8, Black, bitboards, (1<<56)|(1<<17), utils)
	if !attackedRook {
		t.Errorf("A2 should be attacked by Black Rook on A8")
	}
}

func TestBoardStruct(t *testing.T) {
	board := NewBoard()
	setPieceBit(board, White, 0)
	
	if !getPieceBit(board, White, 0) {
		t.Errorf("Expected A1 for White to be true")
	}
	
	clearPieceBit(board, White, 0)
	if getPieceBit(board, White, 0) {
		t.Errorf("Expected A1 for White to be false after clear")
	}
}

func TestGetCastlingMoves(t *testing.T) {
	kingPos := Position{File: FileE, Rank: Rank1} // E1
	
	// Condition: no checks, not moved, no occupancy around, not attacked -> should have 2 moves
	moves := GetCastlingMoves(
		White,
		&kingPos,
		false,
		false,
		true,
		true,
		func(p Position) bool { return false },
		func(p Position, s Side) bool { return false },
	)
	
	if len(moves) != 2 {
		t.Errorf("Expected 2 castling moves, got %d", len(moves))
	}
}
