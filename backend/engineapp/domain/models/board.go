package models

import (
	"math/bits"
	"strings"
)

func SafeShift(val uint64, shift int) uint64 {
	if shift >= 64 || shift <= -64 {
		return 0
	}
	if shift > 0 {
		return val << shift
	}
	return val >> (-shift)
}

func SetBit(bitboard uint64, index int) uint64 {
	return bitboard | (1 << index)
}

func ClearBit(bitboard uint64, index int) uint64 {
	return bitboard & ^(1 << index)
}

func GetBit(bitboard uint64, index int) bool {
	return (bitboard>>index)&1 == 1
}

func CountBits(bitboard uint64) int {
	return bits.OnesCount64(bitboard)
}

func GetRookAttacks(square int, occupancy uint64) uint64 {
	var attacks uint64 = 0
	rank := square / 8
	file := square % 8

	// North
	for r := rank + 1; r < 8; r++ {
		s := r*8 + file
		attacks |= (1 << s)
		if (occupancy & (1 << s)) != 0 {
			break
		}
	}
	// South
	for r := rank - 1; r >= 0; r-- {
		s := r*8 + file
		attacks |= (1 << s)
		if (occupancy & (1 << s)) != 0 {
			break
		}
	}
	// East
	for f := file + 1; f < 8; f++ {
		s := rank*8 + f
		attacks |= (1 << s)
		if (occupancy & (1 << s)) != 0 {
			break
		}
	}
	// West
	for f := file - 1; f >= 0; f-- {
		s := rank*8 + f
		attacks |= (1 << s)
		if (occupancy & (1 << s)) != 0 {
			break
		}
	}
	return attacks
}

func GetBishopAttacks(square int, occupancy uint64) uint64 {
	var attacks uint64 = 0
	rank := square / 8
	file := square % 8

	directions := [][2]int{{1, 1}, {1, -1}, {-1, 1}, {-1, -1}}
	for _, dir := range directions {
		dr, df := dir[0], dir[1]
		r, f := rank+dr, file+df
		for r >= 0 && r < 8 && f >= 0 && f < 8 {
			s := r*8 + f
			attacks |= (1 << s)
			if (occupancy & (1 << s)) != 0 {
				break
			}
			r, f = r+dr, f+df
		}
	}
	return attacks
}

func GetQueenAttacks(square int, occupancy uint64) uint64 {
	return GetRookAttacks(square, occupancy) | GetBishopAttacks(square, occupancy)
}

type BitboardUtils struct {
	FileA uint64
	FileB uint64
	FileC uint64
	FileD uint64
	FileE uint64
	FileF uint64
	FileG uint64
	FileH uint64

	Rank1 uint64
	Rank2 uint64
	Rank3 uint64
	Rank4 uint64
	Rank5 uint64
	Rank6 uint64
	Rank7 uint64
	Rank8 uint64

	KnightMoves      [64]uint64
	KingMoves        [64]uint64
	WhitePawnAttacks [64]uint64
	BlackPawnAttacks [64]uint64
}

func NewBitboardUtils() *BitboardUtils {
	u := &BitboardUtils{}

	u.FileA = 0x0101010101010101
	u.FileB = u.FileA << 1
	u.FileC = u.FileA << 2
	u.FileD = u.FileA << 3
	u.FileE = u.FileA << 4
	u.FileF = u.FileA << 5
	u.FileG = u.FileA << 6
	u.FileH = u.FileA << 7

	u.Rank1 = 0x00000000000000FF
	u.Rank2 = u.Rank1 << 8
	u.Rank3 = u.Rank1 << 16
	u.Rank4 = u.Rank1 << 24
	u.Rank5 = u.Rank1 << 32
	u.Rank6 = u.Rank1 << 40
	u.Rank7 = u.Rank1 << 48
	u.Rank8 = u.Rank1 << 56
	u.initMasks()
	return u
}

const (
	WhiteKingStart     = uint64(1) << 4
	BlackKingStart     = uint64(1) << 60
	WhiteKingSideDest  = uint64(1) << 6
	WhiteQueenSideDest = uint64(1) << 2
	BlackKingSideDest  = uint64(1) << 62
	BlackQueenSideDest = uint64(1) << 58
)

func (u *BitboardUtils) initMasks() {
	for i := range 64 {
		var knightMask uint64 = 0
		// 2 up, 1 left/right
		knightMask |= SafeShift(1<<i, 17) & ^u.FileA
		knightMask |= SafeShift(1<<i, 15) & ^u.FileH
		// 2 down, 1 left/right
		knightMask |= SafeShift(1<<i, -17) & ^u.FileH
		knightMask |= SafeShift(1<<i, -15) & ^u.FileA
		// 1 up, 2 left/right
		knightMask |= SafeShift(1<<i, 10) & ^(u.FileA | u.FileB)
		knightMask |= SafeShift(1<<i, 6) & ^(u.FileG | u.FileH)
		// 1 down, 2 left/right
		knightMask |= SafeShift(1<<i, -10) & ^(u.FileG | u.FileH)
		knightMask |= SafeShift(1<<i, -6) & ^(u.FileA | u.FileB)
		u.KnightMoves[i] = knightMask

		var kingMask uint64 = 0
		kingMask |= SafeShift(1<<i, 1) & ^u.FileA
		kingMask |= SafeShift(1<<i, -1) & ^u.FileH
		kingMask |= SafeShift(1<<i, 8)
		kingMask |= SafeShift(1<<i, -8)
		kingMask |= SafeShift(1<<i, 7) & ^u.FileH
		kingMask |= SafeShift(1<<i, 9) & ^u.FileA
		kingMask |= SafeShift(1<<i, -7) & ^u.FileA
		kingMask |= SafeShift(1<<i, -9) & ^u.FileH
		u.KingMoves[i] = kingMask

		var whiteAttacks uint64 = 0
		if i < 56 {
			if (u.FileA & (1 << i)) == 0 {
				whiteAttacks |= (1 << (i + 7))
			}
			if (u.FileH & (1 << i)) == 0 {
				whiteAttacks |= (1 << (i + 9))
			}
		}
		u.WhitePawnAttacks[i] = whiteAttacks

		var blackAttacks uint64 = 0
		if i > 7 {
			if (u.FileH & (1 << i)) == 0 {
				blackAttacks |= (1 << (i - 7))
			}
			if (u.FileA & (1 << i)) == 0 {
				blackAttacks |= (1 << (i - 9))
			}
		}
		u.BlackPawnAttacks[i] = blackAttacks
	}
}

func ToBitIndex(position Position) int {
	return (int(position.Rank)-1)*8 + int(position.File)
}

func BitIndexToPosition(index int) Position {
	fileIdx := index % 8
	rankIdx := (index / 8) + 1
	return Position{File: File(fileIdx), Rank: Rank(rankIdx)}
}

func BitsToMovements(bitboard uint64, fromIdx *int, fromDelta *int) []Movement {
	var movements []Movement
	for i := range 64 {
		if (bitboard>>i)&1 == 1 {
			toPos := BitIndexToPosition(i)
			var idx int
			if fromIdx != nil {
				idx = *fromIdx
			} else if fromDelta != nil {
				idx = i + *fromDelta
			}
			fromPos := BitIndexToPosition(idx)
			movements = append(movements, Movement{From: fromPos, To: toPos})
		}
	}
	return movements
}

func GetSlidingMoves(pType PieceType, pieces uint64, fullOccupancy uint64, ownOccupancy uint64) []Movement {
	var moves []Movement
	for i := range 64 {
		if (pieces>>i)&1 == 1 {
			var attacks uint64
			switch pType {
			case Rook:
				attacks = GetRookAttacks(i, fullOccupancy)
			case Bishop:
				attacks = GetBishopAttacks(i, fullOccupancy)
			case Queen:
				attacks = GetQueenAttacks(i, fullOccupancy)
			default:
				continue
			}

			validMoves := attacks & ^ownOccupancy
			idx := i
			moves = append(moves, BitsToMovements(validMoves, &idx, nil)...)
		}
	}
	return moves
}

func SetPieceBitBoard(bitIndex int, side Side, pieceType PieceType, bitboards map[PieceKey]uint64, occupancies map[Side]uint64, combinedSide Side) {
	key := PieceKey{Side: side, PieceType: pieceType}
	bitboards[key] = SetBit(bitboards[key], bitIndex)
	occupancies[side] = SetBit(occupancies[side], bitIndex)
	occupancies[combinedSide] = SetBit(occupancies[combinedSide], bitIndex)
}

func ClearPieceBitBoard(bitIndex int, side Side, pieceType PieceType, bitboards map[PieceKey]uint64, occupancies map[Side]uint64, combinedSide Side) {
	key := PieceKey{Side: side, PieceType: pieceType}
	bitboards[key] = ClearBit(bitboards[key], bitIndex)
	occupancies[side] = ClearBit(occupancies[side], bitIndex)
	occupancies[combinedSide] = ClearBit(occupancies[combinedSide], bitIndex)
}

func GetPawnMoves(side Side, pawns uint64, occupancyCombined uint64, occupancyOpponent uint64, utils *BitboardUtils, enPassantTarget string) []Movement {
	var moves []Movement
	emptySquares := ^occupancyCombined

	var singlePush, doublePush, captureLeft, captureRight uint64


	if side == White {
		singlePush = (pawns << 8) & emptySquares
		doublePush = ((pawns & utils.Rank2) << 8 & emptySquares) << 8 & emptySquares
		captureLeft = (pawns << 7) & occupancyOpponent & ^utils.FileH
		captureRight = (pawns << 9) & occupancyOpponent & ^utils.FileA

		if enPassantTarget != "-" {
			epIdx, ok := ParseSquare(enPassantTarget)
			if ok {
				epMask := uint64(1) << epIdx
				captureLeft |= (pawns << 7) & epMask & ^utils.FileH
				captureRight |= (pawns << 9) & epMask & ^utils.FileA
			}
		}

	} else {
		singlePush = (pawns >> 8) & emptySquares
		doublePush = ((pawns & utils.Rank7) >> 8 & emptySquares) >> 8 & emptySquares
		captureLeft = (pawns >> 9) & occupancyOpponent & ^utils.FileH
		captureRight = (pawns >> 7) & occupancyOpponent & ^utils.FileA

		if enPassantTarget != "-" {
			epIdx, ok := ParseSquare(enPassantTarget)
			if ok {
				epMask := uint64(1) << epIdx
				captureLeft |= (pawns >> 9) & epMask & ^utils.FileH
				captureRight |= (pawns >> 7) & epMask & ^utils.FileA
			}
		}
	}


	deltaP1 := -8
	deltaP2 := -16
	deltaL1 := -7
	deltaR1 := -9

	if side == Black {
		deltaP1 = 8
		deltaP2 = 16
		deltaL1 = 9
		deltaR1 = 7
	}

	moves = append(moves, BitsToMovements(singlePush, nil, &deltaP1)...)
	moves = append(moves, BitsToMovements(doublePush, nil, &deltaP2)...)
	moves = append(moves, BitsToMovements(captureLeft, nil, &deltaL1)...)
	moves = append(moves, BitsToMovements(captureRight, nil, &deltaR1)...)

	return moves
}

func GetKnightMoves(pieces uint64, ownOccupancy uint64, utils *BitboardUtils) []Movement {
	var moves []Movement
	for i := range 64 {
		if (pieces>>i)&1 == 1 {
			attacks := utils.KnightMoves[i]
			validMoves := attacks & ^ownOccupancy
			idx := i
			moves = append(moves, BitsToMovements(validMoves, &idx, nil)...)
		}
	}
	return moves
}

func GetKingMoves(pieces uint64, ownOccupancy uint64, utils *BitboardUtils) []Movement {
	var moves []Movement
	for i := range 64 {
		if (pieces>>i)&1 == 1 {
			attacks := utils.KingMoves[i]
			validMoves := attacks & ^ownOccupancy
			idx := i
			moves = append(moves, BitsToMovements(validMoves, &idx, nil)...)
		}
	}
	return moves
}

func GetCastlingMoves(
	side Side,
	kingPos *Position,
	kingMoved bool,
	isCheck bool,
	rookHUnmoved bool,
	rookAUnmoved bool,
	isSquareOccupiedFn func(Position) bool,
	isSquareAttackedFn func(Position, Side) bool,
) []Movement {
	var moves []Movement
	if kingPos == nil || kingMoved || isCheck {
		return moves
	}

	rank := Rank1
	opponentSide := Black
	if side == Black {
		rank = Rank8
		opponentSide = White
	}

	// Kingside
	if rookHUnmoved {
		fPos := Position{File: FileF, Rank: rank}
		gPos := Position{File: FileG, Rank: rank}
		if !isSquareOccupiedFn(fPos) && !isSquareOccupiedFn(gPos) {
			if !isSquareAttackedFn(fPos, opponentSide) {
				moves = append(moves, Movement{From: *kingPos, To: gPos})
			}
		}
	}

	// Queenside
	if rookAUnmoved {
		dPos := Position{File: FileD, Rank: rank}
		cPos := Position{File: FileC, Rank: rank}
		bPos := Position{File: FileB, Rank: rank}
		if !isSquareOccupiedFn(dPos) && !isSquareOccupiedFn(cPos) && !isSquareOccupiedFn(bPos) {
			if !isSquareAttackedFn(dPos, opponentSide) {
				moves = append(moves, Movement{From: *kingPos, To: cPos})
			}
		}
	}

	return moves
}

func GetLsbIndex(bitboard uint64) int {
	if bitboard == 0 {
		return -1
	}
	return bits.TrailingZeros64(bitboard)
}

func IsSquareAttacked(
	squareIndex int,
	attackingSide Side,
	bitboards map[PieceKey]uint64,
	occupancyCombined uint64,
	utils *BitboardUtils,
) bool {
	// Attacked by Pawns
	pawns := bitboards[PieceKey{Side: attackingSide, PieceType: Pawn}]
	if attackingSide == White {
		if (utils.BlackPawnAttacks[squareIndex] & pawns) != 0 {
			return true
		}
	} else {
		if (utils.WhitePawnAttacks[squareIndex] & pawns) != 0 {
			return true
		}
	}

	// Attacked by Knights
	knights := bitboards[PieceKey{Side: attackingSide, PieceType: Knight}]
	if (utils.KnightMoves[squareIndex] & knights) != 0 {
		return true
	}

	// Attacked by King
	king := bitboards[PieceKey{Side: attackingSide, PieceType: King}]
	if (utils.KingMoves[squareIndex] & king) != 0 {
		return true
	}

	// Attacked by Sliders
	rooks := bitboards[PieceKey{Side: attackingSide, PieceType: Rook}]
	queens := bitboards[PieceKey{Side: attackingSide, PieceType: Queen}]
	rooksQueens := rooks | queens
	if (GetRookAttacks(squareIndex, occupancyCombined) & rooksQueens) != 0 {
		return true
	}

	bishops := bitboards[PieceKey{Side: attackingSide, PieceType: Bishop}]
	bishopsQueens := bishops | queens
	if (GetBishopAttacks(squareIndex, occupancyCombined) & bishopsQueens) != 0 {
		return true
	}

	return false
}

// original simple Board struct definition adapted to uint64
type Board struct {
	bitboards map[Side]uint64
}

func NewBoard() Board {
	return Board{
		bitboards: make(map[Side]uint64),
	}
}

func setPieceBit(board Board, side Side, index int) {
	board.bitboards[side] |= (1 << index)
}

func clearPieceBit(board Board, side Side, index int) {
	board.bitboards[side] &= ^(1 << index)
}

func getPieceBit(board Board, side Side, index int) bool {
	return (board.bitboards[side]>>index)&1 == 1
}

// ParseSquare converts a square string like "e2" to a square index 0-63.
func ParseSquare(sq string) (int, bool) {
	if len(sq) != 2 {
		return 0, false
	}
	file := int(sq[0]) - 'a'
	rank := int(sq[1]) - '1'
	if file < 0 || file > 7 || rank < 0 || rank > 7 {
		return 0, false
	}
	return rank*8 + file, true
}

// SquareIndexToString converts a 0-63 index to a square string like "e2"
func SquareIndexToString(index int) string {
	file := index % 8
	rank := index / 8
	return string(rune('a'+file)) + string(rune('1'+rank))
}

// CloneAndApplyMove clones the bitboards and applies a move
func CloneAndApplyMove(bb Bitboards, fromIdx, toIdx int, promotionPiece string) Bitboards {
	newBB := bb
	fromMask := uint64(1) << fromIdx
	toMask := uint64(1) << toIdx
	clearMask := ^toMask

	// Clear destination square if it has a piece (capture)
	newBB.WhitePawns &= clearMask
	newBB.WhiteKnights &= clearMask
	newBB.WhiteBishops &= clearMask
	newBB.WhiteRooks &= clearMask
	newBB.WhiteQueens &= clearMask
	newBB.WhiteKings &= clearMask
	newBB.BlackPawns &= clearMask
	newBB.BlackKnights &= clearMask
	newBB.BlackBishops &= clearMask
	newBB.BlackRooks &= clearMask
	newBB.BlackQueens &= clearMask
	newBB.BlackKings &= clearMask

	// check if en passant
	if (bb.WhitePawns & fromMask) != 0 {
		if (fromIdx%8 != toIdx%8) && (bb.BlackPawns & toMask) == 0 { // Diagonal move to empty square
			newBB.BlackPawns &= ^(uint64(1) << (toIdx - 8))
		}
	} else if (bb.BlackPawns & fromMask) != 0 {
		if (fromIdx%8 != toIdx%8) && (bb.WhitePawns & toMask) == 0 { // Diagonal move to empty square
			newBB.WhitePawns &= ^(uint64(1) << (toIdx + 8))
		}
	}

	// check if castling
	if (bb.WhiteKings & fromMask) != 0 {
		if fromIdx == 4 && toIdx == 6 { // e1 to g1
			newBB.WhiteRooks &= ^(uint64(1) << 7)
			newBB.WhiteRooks |= (uint64(1) << 5)
		} else if fromIdx == 4 && toIdx == 2 { // e1 to c1
			newBB.WhiteRooks &= ^(uint64(1) << 0)
			newBB.WhiteRooks |= (uint64(1) << 3)
		}
	} else if (bb.BlackKings & fromMask) != 0 {
		if fromIdx == 60 && toIdx == 62 { // e8 to g8
			newBB.BlackRooks &= ^(uint64(1) << 63)
			newBB.BlackRooks |= (uint64(1) << 61)
		} else if fromIdx == 60 && toIdx == 58 { // e8 to c8
			newBB.BlackRooks &= ^(uint64(1) << 56)
			newBB.BlackRooks |= (uint64(1) << 59)
		}
	}

	// Move the piece
	if (bb.WhitePawns & fromMask) != 0 && toIdx >= 56 {
		newBB.WhitePawns &= ^fromMask
		switch promotionPiece {
		case "r", "R": newBB.WhiteRooks |= toMask
		case "n", "N": newBB.WhiteKnights |= toMask
		case "b", "B": newBB.WhiteBishops |= toMask
		default: newBB.WhiteQueens |= toMask
		}
	} else if (bb.BlackPawns & fromMask) != 0 && toIdx <= 7 {
		newBB.BlackPawns &= ^fromMask
		switch promotionPiece {
		case "r", "R": newBB.BlackRooks |= toMask
		case "n", "N": newBB.BlackKnights |= toMask
		case "b", "B": newBB.BlackBishops |= toMask
		default: newBB.BlackQueens |= toMask
		}
	} else {
		if (newBB.WhitePawns & fromMask) != 0 { newBB.WhitePawns &= ^fromMask; newBB.WhitePawns |= toMask }
		if (newBB.WhiteKnights & fromMask) != 0 { newBB.WhiteKnights &= ^fromMask; newBB.WhiteKnights |= toMask }
		if (newBB.WhiteBishops & fromMask) != 0 { newBB.WhiteBishops &= ^fromMask; newBB.WhiteBishops |= toMask }
		if (newBB.WhiteRooks & fromMask) != 0 { newBB.WhiteRooks &= ^fromMask; newBB.WhiteRooks |= toMask }
		if (newBB.WhiteQueens & fromMask) != 0 { newBB.WhiteQueens &= ^fromMask; newBB.WhiteQueens |= toMask }
		if (newBB.WhiteKings & fromMask) != 0 { newBB.WhiteKings &= ^fromMask; newBB.WhiteKings |= toMask }
		
		if (newBB.BlackPawns & fromMask) != 0 { newBB.BlackPawns &= ^fromMask; newBB.BlackPawns |= toMask }
		if (newBB.BlackKnights & fromMask) != 0 { newBB.BlackKnights &= ^fromMask; newBB.BlackKnights |= toMask }
		if (newBB.BlackBishops & fromMask) != 0 { newBB.BlackBishops &= ^fromMask; newBB.BlackBishops |= toMask }
		if (newBB.BlackRooks & fromMask) != 0 { newBB.BlackRooks &= ^fromMask; newBB.BlackRooks |= toMask }
		if (newBB.BlackQueens & fromMask) != 0 { newBB.BlackQueens &= ^fromMask; newBB.BlackQueens |= toMask }
		if (newBB.BlackKings & fromMask) != 0 { newBB.BlackKings &= ^fromMask; newBB.BlackKings |= toMask }
	}

	return newBB
}

// ValidateMove generates pseudo-legal moves for the starting square and checks if the destination is included.


func ValidateMove(
	bb Bitboards,
	utils *BitboardUtils,
	sideToMove Side,
	fromStr string,
	toStr string,
	promotionPiece string,
	enPassantTarget string,
	castlingRights string,
) bool {
    bitboards, occupancies, combinedOccupancy := bb.GenerateMaps()

	fromIdx, ok1 := ParseSquare(fromStr)
	toIdx, ok2 := ParseSquare(toStr)
	if !ok1 || !ok2 {
		return false
	}

	enemySide := Black
	if sideToMove == Black {
		enemySide = White
	}

	var pType PieceType
	pieceFound := false
	for _, pt := range []PieceType{Pawn, Knight, Bishop, Rook, Queen, King} {
		key := PieceKey{Side: sideToMove, PieceType: pt}
		if GetBit(bitboards[key], fromIdx) {
			pType = pt
			pieceFound = true
			break
		}
	}

	if !pieceFound {
		return false
	}

	var validMoves []Movement
	pieceBB := uint64(1) << fromIdx
	ownOccupancy := occupancies[sideToMove]
	enemyOccupancy := occupancies[enemySide]

	switch pType {
	case Pawn:
		validMoves = GetPawnMoves(sideToMove, pieceBB, combinedOccupancy, enemyOccupancy, utils, enPassantTarget)
	case Knight:
		validMoves = GetKnightMoves(pieceBB, ownOccupancy, utils)
	case King:
		validMoves = GetKingMoves(pieceBB, ownOccupancy, utils)
		
		fromPos := BitIndexToPosition(fromIdx)
		isCheck := IsSquareAttacked(fromIdx, enemySide, bitboards, combinedOccupancy, utils)
		
		// generate castling moves
		var rookHUnmoved, rookAUnmoved bool
		if sideToMove == White {
		    rookHUnmoved = strings.Contains(castlingRights, "K")
		    rookAUnmoved = strings.Contains(castlingRights, "Q")
		} else {
		    rookHUnmoved = strings.Contains(castlingRights, "k")
		    rookAUnmoved = strings.Contains(castlingRights, "q")
		}
		
		castlingMoves := GetCastlingMoves(
			sideToMove,
			&fromPos,
			false, // assume king moved check is handled by castlingRights string
			isCheck,
			rookHUnmoved,
			rookAUnmoved,
			func(pos Position) bool {
				idx := ToBitIndex(pos)
				return GetBit(combinedOccupancy, idx)
			},
			func(pos Position, side Side) bool {
				idx := ToBitIndex(pos)
				return IsSquareAttacked(idx, side, bitboards, combinedOccupancy, utils)
			},
		)
		validMoves = append(validMoves, castlingMoves...)
	case Rook, Bishop, Queen:
		validMoves = GetSlidingMoves(pType, pieceBB, combinedOccupancy, ownOccupancy)
	}

	toPos := BitIndexToPosition(toIdx)
	for _, m := range validMoves {
		if m.To.File == toPos.File && m.To.Rank == toPos.Rank {
			// Apply move to clone
			newBB := CloneAndApplyMove(bb, fromIdx, toIdx, promotionPiece)
			newMap, _, checkCombined := newBB.GenerateMaps()
			
			// Find king's new position
			kingBB := newMap[PieceKey{Side: sideToMove, PieceType: King}]
			kingIdx := GetLsbIndex(kingBB)
			if kingIdx == -1 {
			    return false // King captured, shouldn't happen but safe guard
			}
			
			// Check if king is attacked
			inCheck := IsSquareAttacked(kingIdx, enemySide, newMap, checkCombined, utils)
			return !inCheck
		}
	}

	return false
}
