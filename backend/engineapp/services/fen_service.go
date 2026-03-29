package services

import (
	"errors"
	"strings"
)

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

// FENToBitboards converts a FEN string to an array of 12 bitboards.
// The array mapping corresponds to:
// [0]: White Pawns   [1]: White Knights [2]: White Bishops
// [3]: White Rooks   [4]: White Queens  [5]: White Kings
// [6]: Black Pawns   [7]: Black Knights [8]: Black Bishops
// [9]: Black Rooks  [10]: Black Queens [11]: Black Kings
func FENToBitboards(fen string) (Bitboards, error) {
	bitboards := Bitboards{}
	parts := strings.Split(fen, " ")
	if len(parts) == 0 {
		return bitboards, errors.New("invalid FEN string")
	}

	ranks := strings.Split(parts[0], "/")
	if len(ranks) != 8 {
		return bitboards, errors.New("invalid FEN board representation")
	}

	for rankIdx, rankStr := range ranks {
		// Rank 0 in FEN corresponds to rank 8 on the board.
		// We process squares so that bit 0 is A1 and bit 63 is H8.
		fileIdx := 0
		for _, char := range rankStr {
			if char >= '1' && char <= '8' {
				fileIdx += int(char - '0')
			} else {
				if fileIdx >= 8 {
					return bitboards, errors.New("invalid FEN string: too many pieces in a rank")
				}

				// A1=0, H1=7, A8=56, H8=63
				square := (7-rankIdx)*8 + fileIdx
				bitMask := uint64(1) << square

				switch char {
				case 'P':
					bitboards.WhitePawns |= bitMask
				case 'N':
					bitboards.WhiteKnights |= bitMask
				case 'B':
					bitboards.WhiteBishops |= bitMask
				case 'R':
					bitboards.WhiteRooks |= bitMask
				case 'Q':
					bitboards.WhiteQueens |= bitMask
				case 'K':
					bitboards.WhiteKings |= bitMask
				case 'p':
					bitboards.BlackPawns |= bitMask
				case 'n':
					bitboards.BlackKnights |= bitMask
				case 'b':
					bitboards.BlackBishops |= bitMask
				case 'r':
					bitboards.BlackRooks |= bitMask
				case 'q':
					bitboards.BlackQueens |= bitMask
				case 'k':
					bitboards.BlackKings |= bitMask
				default:
					return bitboards, errors.New("invalid piece character in FEN")
				}
				fileIdx++
			}
		}
	}
	return bitboards, nil
}
