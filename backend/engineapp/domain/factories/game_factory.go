package factories

import (
	"engineapp/domain/models"
	"errors"
	"fmt"
	"log"
	"strings"
)

func LoadGame(game_id string, status models.GameStatus, format models.GameFormat, mode models.GameMode, lightPlayer *models.Player, darkPlayer *models.Player, fen string, history []string, result string) *models.Game {
	bitboards, err := FENToBitboards(fen)
	if err != nil {
		log.Printf("Failed to convert FEN to bitboards: %v", err)
		return nil
	}

	turn := models.White
	castling := "-"
	enPassant := "-"
	halfMove := 0
	fullMove := 1

	parts := strings.Split(fen, " ")
	if len(parts) > 1 {
		turn = models.ToSide(parts[1])
	}
	if len(parts) > 2 {
		castling = parts[2]
	}
	if len(parts) > 3 {
		enPassant = parts[3]
	}
	if len(parts) > 4 {
		fmt.Sscanf(parts[4], "%d", &halfMove)
	}
	if len(parts) > 5 {
		fmt.Sscanf(parts[5], "%d", &fullMove)
	}

	game := models.LoadGame(game_id, status, format, mode, lightPlayer, darkPlayer, bitboards, turn, history, result, castling, enPassant, halfMove, fullMove)
	return &game
}

// FENToBitboards converts a FEN string to an array of 12 bitboards.
// The array mapping corresponds to:
// [0]: White Pawns   [1]: White Knights [2]: White Bishops
// [3]: White Rooks   [4]: White Queens  [5]: White Kings
// [6]: Black Pawns   [7]: Black Knights [8]: Black Bishops
// [9]: Black Rooks  [10]: Black Queens [11]: Black Kings
func FENToBitboards(fen string) (models.Bitboards, error) {
	bitboards := models.Bitboards{}
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
