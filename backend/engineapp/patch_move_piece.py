import re

with open("models/game.go", "r") as f:
    content = f.read()

# Replace the end of MovePiece to actually apply the move
old_end = """	// check move is legal
	isValid := ValidateMove(g.Bitboards, utils, sideToMove, move.From, move.To, "q", g.EnPassantTarget, g.CastlingRights)
	if !isValid {
		return MoveValidationResult{Valid: false, Error: "Illegal move"}
	}

	return MoveValidationResult{Valid: true}
}"""

new_end = """	// check move is legal
	isValid := ValidateMove(g.Bitboards, utils, sideToMove, move.From, move.To, "q", g.EnPassantTarget, g.CastlingRights)
	if !isValid {
		return MoveValidationResult{Valid: false, Error: "Illegal move"}
	}

	// Apply the move
	g.Bitboards = CloneAndApplyMove(g.Bitboards, fromIdx, toIdx, "q")
	
	// Toggle Turn
	if g.turn == White {
		g.turn = Black
	} else {
		g.turn = White
		g.FullmoveNumber++
	}

	// Update HalfmoveClock (reset on pawn move or capture)
	isCapture := false
	for _, pt := range []PieceType{Pawn, Knight, Bishop, Rook, Queen, King} {
		if GetBit(occupancies[g.turn], toIdx) { // actually g.turn is now the enemy, so occupancies[enemySide]
			isCapture = true
			break
		}
	}
	if fromPieceType == Pawn || isCapture {
		g.HalfmoveClock = 0
	} else {
		g.HalfmoveClock++
	}

	// Update EnPassantTarget
	g.EnPassantTarget = "-"
	if fromPieceType == Pawn {
		if sideToMove == White && toIdx-fromIdx == 16 {
			g.EnPassantTarget = SquareIndexToString(fromIdx + 8)
		} else if sideToMove == Black && fromIdx-toIdx == 16 {
			g.EnPassantTarget = SquareIndexToString(fromIdx - 8)
		}
	}

	// Update CastlingRights
	if g.CastlingRights != "-" {
		if fromPieceType == King {
			if sideToMove == White {
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "")
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "")
			} else {
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "")
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "")
			}
		} else if fromPieceType == Rook {
			if sideToMove == White {
				if fromIdx == 7 { g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "") } // h1
				if fromIdx == 0 { g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "") } // a1
			} else {
				if fromIdx == 63 { g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "") } // h8
				if fromIdx == 56 { g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "") } // a8
			}
		}
		if g.CastlingRights == "" {
			g.CastlingRights = "-"
		}
	}

	return MoveValidationResult{Valid: true}
}"""

content = content.replace(old_end, new_end)

with open("models/game.go", "w") as f:
    f.write(content)
