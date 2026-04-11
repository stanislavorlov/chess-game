package models

import (
	"engineapp/handlers/ws"
	"strings"
)

type Game struct {
	game_id   string
	status    GameStatus
	format    GameFormat
	Bitboards Bitboards
	turn      Side
	result    string
}

type GameFormat struct {
	name              string
	minutes           int
	move_increment_ms int
}

func NewGameFormat(name string, minutes int, moveIncrementMs int) GameFormat {
	return GameFormat{
		name:              name,
		minutes:           minutes,
		move_increment_ms: moveIncrementMs,
	}
}

var (
	Bullet_1_0 GameFormat = GameFormat{name: "bullet", minutes: 1, move_increment_ms: 0}
	Bullet_1_1 GameFormat = GameFormat{name: "bullet", minutes: 1, move_increment_ms: 1}
	Bullet_2_1 GameFormat = GameFormat{name: "bullet", minutes: 2, move_increment_ms: 1}
	Bullet_3_0 GameFormat = GameFormat{name: "bullet", minutes: 3, move_increment_ms: 0}
	Bullet_3_2 GameFormat = GameFormat{name: "bullet", minutes: 3, move_increment_ms: 2}

	Blitz_3_0 GameFormat = GameFormat{name: "blitz", minutes: 3, move_increment_ms: 0}
	Blitz_3_2 GameFormat = GameFormat{name: "blitz", minutes: 3, move_increment_ms: 2}
	Blitz_5_0 GameFormat = GameFormat{name: "blitz", minutes: 5, move_increment_ms: 0}
	Blitz_5_3 GameFormat = GameFormat{name: "blitz", minutes: 5, move_increment_ms: 3}

	Rapid_10_0  GameFormat = GameFormat{name: "rapid", minutes: 10, move_increment_ms: 0}
	Rapid_10_5  GameFormat = GameFormat{name: "rapid", minutes: 10, move_increment_ms: 5}
	Rapid_15_10 GameFormat = GameFormat{name: "rapid", minutes: 15, move_increment_ms: 10}

	Classical_30_0  GameFormat = GameFormat{name: "classical", minutes: 30, move_increment_ms: 0}
	Classical_30_20 GameFormat = GameFormat{name: "classical", minutes: 30, move_increment_ms: 20}
	Classical_45_45 GameFormat = GameFormat{name: "classical", minutes: 45, move_increment_ms: 45}
)

type GameStatus string

const (
	Created            GameStatus = "created"
	Started            GameStatus = "started"
	Finished           GameStatus = "finished"
	Aborted            GameStatus = "aborted"
	FEN_START_POSITION string     = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

type MoveValidationResult struct {
	Valid bool
	Error string
}

func LoadGame(game_id string, status GameStatus, format GameFormat, bitboards Bitboards, turn Side, result string) Game {
	return Game{
		game_id:   game_id,
		status:    status,
		format:    format,
		Bitboards: bitboards,
		turn:      turn,
		result:    result,
	}
}

/*func NewGame() Game {
	return Game{
		game_id:   uuid.New().String(),
		status:    Created,
		bitboards: NewBitboards(),
	}
}*/

func (g *Game) StartGame() {
	g.status = Started
}

func (g *Game) FinishGame() {
	g.status = Finished
}

func (g *Game) IsActive() bool {
	return g.status == Started
}

func (g *Game) MovePiece(move ws.GameRequest) MoveValidationResult {
	if !g.IsActive() {
		return MoveValidationResult{Valid: false, Error: "Game has not started"}
	}

	bbMap, occupancies, _ := g.Bitboards.GenerateMaps()

	utils := NewBitboardUtils()
	sideToMove := g.turn

	fromIdx, ok1 := ParseSquare(move.From)
	toIdx, ok2 := ParseSquare(move.To)
	if !ok1 || !ok2 {
		return MoveValidationResult{Valid: false, Error: "Invalid square"}
	}

	var fromSide Side
	var fromPieceType PieceType
	pieceFound := false

	for _, pt := range []PieceType{Pawn, Knight, Bishop, Rook, Queen, King} {
		if GetBit(bbMap[PieceKey{Side: White, PieceType: pt}], fromIdx) {
			fromSide = White
			fromPieceType = pt
			pieceFound = true
			break
		}
		if GetBit(bbMap[PieceKey{Side: Black, PieceType: pt}], fromIdx) {
			fromSide = Black
			fromPieceType = pt
			pieceFound = true
			break
		}
	}

	// check move.From's piece exists
	if !pieceFound {
		return MoveValidationResult{Valid: false, Error: "No piece at the source square"}
	}

	// check if turn is followed
	if fromSide != sideToMove {
		return MoveValidationResult{Valid: false, Error: "Not your turn"}
	}

	// check move.Piece correspond to the board's piece
	if pieceStr := move.Piece.PieceType; len(pieceStr) == 2 {
		expectedPiece := string(fromSide) + string(fromPieceType)
		if pieceStr != expectedPiece {
			return MoveValidationResult{Valid: false, Error: "Piece on board does not match the move's piece"}
		}
	}

	// check move.To's piece is empty or opponent's piece
	if GetBit(occupancies[sideToMove], toIdx) {
		return MoveValidationResult{Valid: false, Error: "Cannot capture your own piece"}
	}

	// check move is legal
	isValid := ValidateMove(g.Bitboards, utils, sideToMove, move.From, move.To)
	if !isValid {
		return MoveValidationResult{Valid: false, Error: "Illegal move"}
	}

	return MoveValidationResult{Valid: true}
}

// FEN returns the current board state in FEN notation
func (g *Game) FEN() string {
	pieceMap, _, _ := g.Bitboards.GenerateMaps()
	var fen strings.Builder

	pieceChars := map[PieceType]map[Side]string{
		Pawn:   {White: "P", Black: "p"},
		Knight: {White: "N", Black: "n"},
		Bishop: {White: "B", Black: "b"},
		Rook:   {White: "R", Black: "r"},
		Queen:  {White: "Q", Black: "q"},
		King:   {White: "K", Black: "k"},
	}

	for rank := 7; rank >= 0; rank-- {
		emptyCount := 0
		for file := range 8 {
			sqIdx := rank*8 + file
			found := false

			for pt, sides := range pieceChars {
				if GetBit(pieceMap[PieceKey{Side: White, PieceType: pt}], sqIdx) {
					if emptyCount > 0 {
						fen.WriteString(string(rune('0' + emptyCount)))
						emptyCount = 0
					}
					fen.WriteString(sides[White])
					found = true
					break
				}
				if GetBit(pieceMap[PieceKey{Side: Black, PieceType: pt}], sqIdx) {
					if emptyCount > 0 {
						fen.WriteString(string(rune('0' + emptyCount)))
						emptyCount = 0
					}
					fen.WriteString(sides[Black])
					found = true
					break
				}
			}

			if !found {
				emptyCount++
			}
		}
		if emptyCount > 0 {
			fen.WriteString(string(rune('0' + emptyCount)))
		}
		if rank > 0 {
			fen.WriteString("/")
		}
	}

	turnStr := "w"
	if g.turn == Black {
		turnStr = "b"
	}

	// Default castling, en passant, half and full move to initial-like values
	fen.WriteString(" " + turnStr + " - - 0 1")
	return fen.String()
}

// Turn returns the side to move
func (g *Game) Turn() string {
	if g.turn == White {
		return "w"
	}
	return "b"
}

func (g *Game) Winner() string {
	return ""
}

// LegalMoves returns a list of legal moves in standard notation like "e2e4"
func (g *Game) LegalMoves() []string {
	utils := NewBitboardUtils()
	bbMap, occupancies, combinedOccupancy := g.Bitboards.GenerateMaps()

	enemySide := Black
	if g.turn == Black {
		enemySide = White
	}

	var moves []string

	for i := 0; i < 64; i++ {
		// find pieces belonging to current turn
		var pType PieceType
		found := false
		for _, pt := range []PieceType{Pawn, Knight, Bishop, Rook, Queen, King} {
			if GetBit(bbMap[PieceKey{Side: g.turn, PieceType: pt}], i) {
				pType = pt
				found = true
				break
			}
		}
		if !found {
			continue
		}

		pieceBB := uint64(1) << i
		ownOccupancy := occupancies[g.turn]
		enemyOccupancy := occupancies[enemySide]

		var pseudoMoves []Movement
		switch pType {
		case Pawn:
			pseudoMoves = GetPawnMoves(g.turn, pieceBB, combinedOccupancy, enemyOccupancy, utils)
		case Knight:
			pseudoMoves = GetKnightMoves(pieceBB, ownOccupancy, utils)
		case King:
			pseudoMoves = GetKingMoves(pieceBB, ownOccupancy, utils)
		case Rook, Bishop, Queen:
			pseudoMoves = GetSlidingMoves(pType, pieceBB, combinedOccupancy, ownOccupancy)
		}

		fromStr := SquareIndexToString(i)
		for _, m := range pseudoMoves {
			toIdx := ToBitIndex(m.To)
			toStr := SquareIndexToString(toIdx)
			// Apply move to clone
			newBB := CloneAndApplyMove(g.Bitboards, i, toIdx)
			newMap, _, checkCombined := newBB.GenerateMaps()

			kingBB := newMap[PieceKey{Side: g.turn, PieceType: King}]
			kingIdx := GetLsbIndex(kingBB)
			if kingIdx == -1 {
				continue
			}

			inCheck := IsSquareAttacked(kingIdx, enemySide, newMap, checkCombined, utils)
			if !inCheck {
				moves = append(moves, fromStr+toStr)
			}
		}
	}

	return moves
}

// IsCheck returns true if the current turn's king is attacked
func (g *Game) IsCheck() bool {
	utils := NewBitboardUtils()
	bbMap, _, combinedOccupancy := g.Bitboards.GenerateMaps()

	kingBB := bbMap[PieceKey{Side: g.turn, PieceType: King}]
	kingIdx := GetLsbIndex(kingBB)
	if kingIdx == -1 {
		return false
	}

	enemySide := Black
	if g.turn == Black {
		enemySide = White
	}

	return IsSquareAttacked(kingIdx, enemySide, bbMap, combinedOccupancy, utils)
}

// IsCheckmate returns true if in check and no legal moves exist
func (g *Game) IsCheckmate() bool {
	return g.IsCheck() && len(g.LegalMoves()) == 0
}

// IsStalemate returns true if not in check and no legal moves exist
func (g *Game) IsStalemate() bool {
	return !g.IsCheck() && len(g.LegalMoves()) == 0
}

// IsDraw returns true if game is mathematically drawn or explicitly marked as draw
func (g *Game) IsDraw() bool {
	return g.IsStalemate() || g.result == "draw"
}
