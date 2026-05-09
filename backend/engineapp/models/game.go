package models

import (
	"engineapp/handlers/ws"
	"fmt"
	"strings"
)

type Game struct {
	game_id         string
	status          GameStatus
	format          GameFormat
	mode            string
	Bitboards       Bitboards
	turn            Side
	history         []string
	result          string
	CastlingRights  string
	EnPassantTarget string
	HalfmoveClock   int
	FullmoveNumber  int
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

func LoadGame(game_id string, status GameStatus, format GameFormat, mode string, bitboards Bitboards, turn Side, history []string, result string, castlingRights string, enPassantTarget string, halfmoveClock int, fullmoveNumber int) Game {
	return Game{
		game_id:         game_id,
		status:          status,
		format:          format,
		mode:            mode,
		Bitboards:       bitboards,
		turn:            turn,
		history:         history,
		result:          result,
		CastlingRights:  castlingRights,
		EnPassantTarget: enPassantTarget,
		HalfmoveClock:   halfmoveClock,
		FullmoveNumber:  fullmoveNumber,
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

func (g *Game) ID() string {
	return g.game_id
}

func (g *Game) Status() GameStatus {
	return g.status
}

func (g *Game) Format() GameFormat {
	return g.format
}

func (g *Game) FormatName() string {
	return g.format.name
}

func (g *Game) FormatMinutes() int {
	return g.format.minutes
}

func (g *Game) Mode() string {
	return g.mode
}

func (g *Game) FormatIncrement() int {
	return g.format.move_increment_ms
}

func (g *Game) Result() string {
	return g.result
}

func (g *Game) History() string {
	return strings.Join(g.history, ",")
}

func (g *Game) HistoryCount() int {
	return len(g.history)
}

func (g *Game) CheckPosition() *string {
	if !g.IsCheck() {
		return nil
	}
	bbMap, _, _ := g.Bitboards.GenerateMaps()
	kingBB := bbMap[PieceKey{Side: g.turn, PieceType: King}]
	kingIdx := GetLsbIndex(kingBB)
	if kingIdx == -1 {
		return nil
	}
	pos := SquareIndexToString(kingIdx)
	return &pos
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
	enemySide := Black
	if sideToMove == Black {
		enemySide = White
	}
	isCapture := GetBit(occupancies[enemySide], toIdx)
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
		switch fromPieceType {
		case King:
			if sideToMove == White {
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "")
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "")
			} else {
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "")
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "")
			}
		case Rook:
			if sideToMove == White {
				if fromIdx == 7 {
					g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "")
				} // h1
				if fromIdx == 0 {
					g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "")
				} // a1
			} else {
				if fromIdx == 63 {
					g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "")
				} // h8
				if fromIdx == 56 {
					g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "")
				} // a8
			}
		}
		if g.CastlingRights == "" {
			g.CastlingRights = "-"
		}
	}

	g.history = append(g.history, move.From+move.To)

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

	fen.WriteString(fmt.Sprintf(" %s %s %s %d %d", turnStr, g.CastlingRights, g.EnPassantTarget, g.HalfmoveClock, g.FullmoveNumber))
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
			pseudoMoves = GetPawnMoves(g.turn, pieceBB, combinedOccupancy, enemyOccupancy, utils, g.EnPassantTarget)
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
			newBB := CloneAndApplyMove(g.Bitboards, i, toIdx, "q")
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
