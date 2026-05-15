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
	lightPlayer     string
	darkPlayer      string
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
	Valid            bool
	Error            string
	IsCastling       bool
	IsKingside       bool
	CastlingRookFrom string
	CastlingRookTo   string
	IsCapture        bool
	CapturedPiece    string
}

func LoadGame(game_id string, status GameStatus, format GameFormat, mode string, lightPlayer string, darkPlayer string, bitboards Bitboards, turn Side, history []string, result string, castlingRights string, enPassantTarget string, halfmoveClock int, fullmoveNumber int) Game {
	return Game{
		game_id:         game_id,
		status:          status,
		format:          format,
		mode:            mode,
		lightPlayer:     lightPlayer,
		darkPlayer:      darkPlayer,
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

func (g *Game) StartGame() {
	g.status = Started
}

func (g *Game) FinishGame() {
	g.status = Finished
}

func (g *Game) SetResult(result string) {
	g.result = result
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

func (g *Game) LightPlayer() string {
	return g.lightPlayer
}

func (g *Game) DarkPlayer() string {
	return g.darkPlayer
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

func (g *Game) opponentTurn() Side {
	if g.turn == White {
		return Black
	}
	return White
}

func (g *Game) identifyPieceAt(idx int, bbMap map[PieceKey]uint64, occupancies map[Side]uint64) (Side, PieceType, bool) {
	mask := uint64(1) << idx
	var side Side
	if (occupancies[White] & mask) != 0 {
		side = White
	} else if (occupancies[Black] & mask) != 0 {
		side = Black
	} else {
		return "", "", false
	}

	for _, pt := range AllPieceTypes {
		if (bbMap[PieceKey{Side: side, PieceType: pt}] & mask) != 0 {
			return side, pt, true
		}
	}
	return "", "", false
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

	fromSide, fromPieceType, pieceFound := g.identifyPieceAt(fromIdx, bbMap, occupancies)

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
	if !ValidateMove(g.Bitboards, utils, sideToMove, move.From, move.To, "q", g.EnPassantTarget, g.CastlingRights) {
		return MoveValidationResult{Valid: false, Error: "Illegal move"}
	}

	isCastling, isKingside, rookFrom, rookTo := g.detectCastling(fromPieceType, sideToMove, fromIdx, toIdx)

	// Apply the move
	g.Bitboards = CloneAndApplyMove(g.Bitboards, fromIdx, toIdx, "q")

	// Update HalfmoveClock (reset on pawn move or capture)
	enemySide := g.opponentTurn()
	toMask := uint64(1) << toIdx
	isCapture := (occupancies[enemySide] & toMask) != 0
	if fromPieceType == Pawn || isCapture {
		g.HalfmoveClock = 0
	} else {
		g.HalfmoveClock++
	}

	g.updateGameMetadata(fromPieceType, sideToMove, fromIdx, toIdx)
	g.history = append(g.history, move.From+move.To)

	// Toggle Turn
	if g.turn == White {
		g.turn = Black
	} else {
		g.turn = White
		g.FullmoveNumber++
	}

	capturedPieceStr := ""
	if isCapture {
		_, capType, _ := g.identifyPieceAt(toIdx, bbMap, occupancies)
		capturedPieceStr = string(enemySide) + string(capType)
	}

	return MoveValidationResult{
		Valid:            true,
		IsCastling:       isCastling,
		IsKingside:       isKingside,
		CastlingRookFrom: rookFrom,
		CastlingRookTo:   rookTo,
		IsCapture:        isCapture,
		CapturedPiece:    capturedPieceStr,
	}
}

func (g *Game) detectCastling(pType PieceType, side Side, fromIdx, toIdx int) (bool, bool, string, string) {
	if pType != King {
		return false, false, "", ""
	}

	fromMask := uint64(1) << fromIdx
	toMask := uint64(1) << toIdx

	if side == White {
		if fromMask == WhiteKingStart {
			switch toMask {
			case WhiteKingSideDest:
				return true, true, "h1", "f1"
			case WhiteQueenSideDest:
				return true, false, "a1", "d1"
			}
		}
	} else {
		if fromMask == BlackKingStart {
			switch toMask {
			case BlackKingSideDest:
				return true, true, "h8", "f8"
			case BlackQueenSideDest:
				return true, false, "a8", "d8"
			}
		}
	}
	return false, false, "", ""
}

func (g *Game) updateGameMetadata(pType PieceType, side Side, fromIdx, toIdx int) {
	utils := NewBitboardUtils()
	fromMask := uint64(1) << fromIdx
	toMask := uint64(1) << toIdx

	// Update EnPassantTarget
	g.EnPassantTarget = "-"
	if pType == Pawn {
		if side == White {
			if (fromMask&utils.Rank2) != 0 && (toMask&utils.Rank4) != 0 {
				g.EnPassantTarget = SquareIndexToString(fromIdx + 8)
			}
		} else {
			if (fromMask&utils.Rank7) != 0 && (toMask&utils.Rank5) != 0 {
				g.EnPassantTarget = SquareIndexToString(fromIdx - 8)
			}
		}
	}

	// Update CastlingRights
	if g.CastlingRights == "-" {
		return
	}

	switch pType {
	case King:
		if side == White {
			g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "")
			g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "")
		} else {
			g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "")
			g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "")
		}
	case Rook:
		if side == White {
			switch fromIdx {
			case 7:
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "K", "")
			case 0:
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "Q", "")
			}
		} else {
			switch fromIdx {
			case 63:
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "k", "")
			case 56:
				g.CastlingRights = strings.ReplaceAll(g.CastlingRights, "q", "")
			}
		}
	}

	if g.CastlingRights == "" {
		g.CastlingRights = "-"
	}
}

// FEN returns the current board state in FEN notation
func (g *Game) FEN() string {
	pieceMap, _, _ := g.Bitboards.GenerateMaps()
	var fen strings.Builder

	for rank := 7; rank >= 0; rank-- {
		emptyCount := 0
		for file := range 8 {
			sqIdx := rank*8 + file
			found := false

			for _, pt := range AllPieceTypes {
				if GetBit(pieceMap[PieceKey{Side: White, PieceType: pt}], sqIdx) {
					if emptyCount > 0 {
						fen.WriteString(string(rune('0' + emptyCount)))
						emptyCount = 0
					}
					fen.WriteString(pt.Symbol(White))
					found = true
					break
				}
				if GetBit(pieceMap[PieceKey{Side: Black, PieceType: pt}], sqIdx) {
					if emptyCount > 0 {
						fen.WriteString(string(rune('0' + emptyCount)))
						emptyCount = 0
					}
					fen.WriteString(pt.Symbol(Black))
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

	fmt.Fprintf(&fen, " %s %s %s %d %d", g.Turn(), g.CastlingRights, g.EnPassantTarget, g.HalfmoveClock, g.FullmoveNumber)
	return fen.String()
}

// Turn returns the side to move
func (g *Game) Turn() string {
	return string(g.turn)
}

func (g *Game) Winner() string {
	return ""
}

// LegalMoves returns a list of legal moves in standard notation like "e2e4"
func (g *Game) LegalMoves() []string {
	utils := NewBitboardUtils()
	bbMap, occupancies, combinedOccupancy := g.Bitboards.GenerateMaps()

	sideToMove := g.turn
	enemySide := g.opponentTurn()
	ownOccupancy := occupancies[sideToMove]
	enemyOccupancy := occupancies[enemySide]

	var moves []string

	// Iterate over each square that has a piece of the current turn
	for i := 0; i < 64; i++ {
		if !GetBit(ownOccupancy, i) {
			continue
		}

		// Find piece type at this square
		var pType PieceType
		found := false
		for _, pt := range AllPieceTypes {
			if GetBit(bbMap[PieceKey{Side: sideToMove, PieceType: pt}], i) {
				pType = pt
				found = true
				break
			}
		}
		if !found {
			continue
		}

		pieceBB := uint64(1) << i
		var pseudoMoves []Movement
		switch pType {
		case Pawn:
			pseudoMoves = GetPawnMoves(sideToMove, pieceBB, combinedOccupancy, enemyOccupancy, utils, g.EnPassantTarget)
		case Knight:
			pseudoMoves = GetKnightMoves(pieceBB, ownOccupancy, utils)
		case King:
			pseudoMoves = GetKingMoves(pieceBB, ownOccupancy, utils)

			fromPos := BitIndexToPosition(i)
			isCheck := IsSquareAttacked(i, enemySide, bbMap, combinedOccupancy, utils)

			var rookHUnmoved, rookAUnmoved bool
			if sideToMove == White {
				rookHUnmoved = strings.Contains(g.CastlingRights, "K")
				rookAUnmoved = strings.Contains(g.CastlingRights, "Q")
			} else {
				rookHUnmoved = strings.Contains(g.CastlingRights, "k")
				rookAUnmoved = strings.Contains(g.CastlingRights, "q")
			}

			castlingMoves := GetCastlingMoves(
				sideToMove,
				&fromPos,
				false,
				isCheck,
				rookHUnmoved,
				rookAUnmoved,
				func(pos Position) bool {
					idx := ToBitIndex(pos)
					return GetBit(combinedOccupancy, idx)
				},
				func(pos Position, side Side) bool {
					idx := ToBitIndex(pos)
					return IsSquareAttacked(idx, side, bbMap, combinedOccupancy, utils)
				},
			)
			pseudoMoves = append(pseudoMoves, castlingMoves...)
		case Rook, Bishop, Queen:
			pseudoMoves = GetSlidingMoves(pType, pieceBB, combinedOccupancy, ownOccupancy)
		}

		fromStr := SquareIndexToString(i)
		for _, m := range pseudoMoves {
			toIdx := ToBitIndex(m.To)
			toStr := SquareIndexToString(toIdx)
			// Apply move to clone and check if king is safe
			newBB := CloneAndApplyMove(g.Bitboards, i, toIdx, "q")
			newMap, _, checkCombined := newBB.GenerateMaps()

			kingBB := newMap[PieceKey{Side: sideToMove, PieceType: King}]
			kingIdx := GetLsbIndex(kingBB)
			if kingIdx != -1 {
				if !IsSquareAttacked(kingIdx, enemySide, newMap, checkCombined, utils) {
					moves = append(moves, fromStr+toStr)
				}
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

	return IsSquareAttacked(kingIdx, g.opponentTurn(), bbMap, combinedOccupancy, utils)
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
