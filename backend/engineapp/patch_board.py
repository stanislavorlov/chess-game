import re

with open("models/board.go", "r") as f:
    content = f.read()

# Patch GetPawnMoves
content = re.sub(
    r"func GetPawnMoves\(side Side, pawns uint64, occupancyCombined uint64, occupancyOpponent uint64, utils \*BitboardUtils\) \[\]Movement \{",
    "func GetPawnMoves(side Side, pawns uint64, occupancyCombined uint64, occupancyOpponent uint64, utils *BitboardUtils, enPassantTarget string) []Movement {",
    content
)

ep_white = """
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
"""

ep_black = """
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
"""

content = re.sub(
    r"\tif side == White \{\n\s+singlePush = \(pawns << 8\) & emptySquares\n\s+doublePush = \(\(pawns & utils\.Rank2\) << 8 & emptySquares\) << 8 & emptySquares\n\s+captureLeft = \(pawns << 7\) & occupancyOpponent & \^utils\.FileH\n\s+captureRight = \(pawns << 9\) & occupancyOpponent & \^utils\.FileA\n",
    ep_white,
    content
)

content = re.sub(
    r"\t\} else \{\n\s+singlePush = \(pawns >> 8\) & emptySquares\n\s+doublePush = \(\(pawns & utils\.Rank7\) >> 8 & emptySquares\) >> 8 & emptySquares\n\s+captureLeft = \(pawns >> 9\) & occupancyOpponent & \^utils\.FileH\n\s+captureRight = \(pawns >> 7\) & occupancyOpponent & \^utils\.FileA\n\t\}",
    ep_black,
    content
)

# Replace CloneAndApplyMove entirely
clone_apply_old = r"// CloneAndApplyMove clones the bitboards and applies a move\nfunc CloneAndApplyMove\(bb Bitboards, fromIdx, toIdx int\) Bitboards \{[\s\S]*?return newBB\n\}"

clone_apply_new = """// CloneAndApplyMove clones the bitboards and applies a move
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
}"""
content = re.sub(clone_apply_old, clone_apply_new, content)

# Patch ValidateMove signature
val_old = """func ValidateMove(
	bb Bitboards,
	utils *BitboardUtils,
	sideToMove Side,
	fromStr string,
	toStr string,
) bool {"""
val_new = """import "strings"

func ValidateMove(
	bb Bitboards,
	utils *BitboardUtils,
	sideToMove Side,
	fromStr string,
	toStr string,
	promotionPiece string,
	enPassantTarget string,
	castlingRights string,
) bool {"""
content = content.replace(val_old, val_new)

# Inside ValidateMove: GetPawnMoves call
content = content.replace(
    "validMoves = GetPawnMoves(sideToMove, pieceBB, combinedOccupancy, enemyOccupancy, utils)",
    "validMoves = GetPawnMoves(sideToMove, pieceBB, combinedOccupancy, enemyOccupancy, utils, enPassantTarget)"
)

# Inside ValidateMove: Castling
content = content.replace(
    "case King:\n\t\tvalidMoves = GetKingMoves(pieceBB, ownOccupancy, utils)",
    """case King:
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
		validMoves = append(validMoves, castlingMoves...)"""
)

# Inside ValidateMove: CloneAndApplyMove
content = content.replace(
    "newBB := CloneAndApplyMove(bb, fromIdx, toIdx)",
    "newBB := CloneAndApplyMove(bb, fromIdx, toIdx, promotionPiece)"
)


with open("models/board.go", "w") as f:
    f.write(content)

