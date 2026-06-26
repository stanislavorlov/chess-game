package models

import (
	"testing"
)

func TestGame_MovePiece_Basic(t *testing.T) {
	bitboards := Bitboards{
		WhitePawns: 0x000000000000FF00,
		WhiteRooks: 0x0000000000000081,
		WhiteKings: 0x0000000000000010,
		BlackPawns: 0x00FF000000000000,
		BlackKings: 0x1000000000000000,
	}
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	game.MovePiece("e2", "e4", "wP")
	_, success := game.PopEvents()

	if !success {
		t.Errorf("Expected move e2e4 to be valid")
	}
	if game.Turn() != "b" {
		t.Errorf("Expected turn to be black after white move, got %s", game.Turn())
	}
}

func TestGame_MovePiece_Castling(t *testing.T) {
	bitboards := Bitboards{
		WhiteRooks: 0x0000000000000081,
		WhiteKings: 0x0000000000000010,
		BlackKings: 0x1000000000000000,
	}
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	game.MovePiece("e1", "g1", "wK")
	events, success := game.PopEvents()

	if !success {
		t.Fatalf("Expected castling to be valid")
	}
	
	hasCastle := false
	for _, e := range events {
		if ce, ok := e.(KingCastledEvent); ok {
			hasCastle = true
			if ce.RookFrom != "h1" || ce.RookTo != "f1" {
				t.Errorf("Expected rook move h1->f1, got %s->%s", ce.RookFrom, ce.RookTo)
			}
		}
	}
	if !hasCastle {
		t.Errorf("Expected IsCastling to be true")
	}

	if game.CastlingRights == "KQkq" || game.CastlingRights == "Kkq" {
		t.Errorf("Expected white castling rights to be removed, got %s", game.CastlingRights)
	}
}

func TestGame_IsCheck(t *testing.T) {
	bitboards := Bitboards{
		WhiteRooks: 0x0000000000000008,
		WhiteKings: 0x0000000000000001,
		BlackKings: 0x0800000000000000,
	}
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "-", "-", 0, 1)

	if !game.IsCheck() {
		t.Errorf("Expected black king to be in check")
	}
}

func TestGame_IsCheckmate(t *testing.T) {
	bitboards := Bitboards{
		WhiteRooks: (uint64(1) << 56) | (uint64(1) << 48),
		BlackKings: (uint64(1) << 63),
		WhiteKings: (uint64(1) << 0),
	}
	game := LoadGame("mate-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "-", "-", 0, 1)

	if !game.IsCheck() {
		t.Errorf("Expected check")
	}
	if !game.IsCheckmate() {
		t.Errorf("Expected checkmate")
	}
}

func TestGame_IsStalemate(t *testing.T) {
	bitboards := Bitboards{
		WhiteKings:  (uint64(1) << 0),
		WhiteQueens: (uint64(1) << 50),
		BlackKings:  (uint64(1) << 56),
	}
	game := LoadGame("stalemate-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "-", "-", 0, 1)

	if game.IsCheck() {
		t.Errorf("Expected NOT in check")
	}
	if !game.IsStalemate() {
		t.Errorf("Expected stalemate")
	}
}

func TestGame_FEN(t *testing.T) {
	bitboards := Bitboards{
		WhiteKings: (uint64(1) << 4),
		BlackKings: (uint64(1) << 60),
	}
	game := LoadGame("fen-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	expectedStart := "4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1"
	if game.FEN() != expectedStart {
		t.Errorf("Expected FEN %s, got %s", expectedStart, game.FEN())
	}
}

func TestGame_MovePiece_Capture(t *testing.T) {
	bitboards := Bitboards{
		WhiteRooks: (uint64(1) << 0),
		WhiteKings: (uint64(1) << 4),
		BlackPawns: (uint64(1) << 56),
		BlackKings: (uint64(1) << 60),
	}
	game := LoadGame("capture-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "-", "-", 0, 1)

	game.MovePiece("a1", "a8", "wR")
	events, success := game.PopEvents()

	if !success {
		t.Fatalf("Expected capture to be valid")
	}
	
	hasCap := false
	for _, e := range events {
		if ce, ok := e.(PieceCapturedEvent); ok {
			hasCap = true
			if ce.Captured != "bP" {
				t.Errorf("Expected captured piece bP, got %s", ce.Captured)
			}
		}
	}
	if !hasCap {
		t.Errorf("Expected IsCapture to be true")
	}
}

func TestGame_MovePiece_EnPassant(t *testing.T) {
	bitboards := Bitboards{
		WhitePawns: (uint64(1) << 36),
		WhiteKings: (uint64(1) << 4),
		BlackPawns: (uint64(1) << 35),
		BlackKings: (uint64(1) << 60),
	}
	game := LoadGame("ep-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{"d7d5"}, "", "-", "d6", 0, 1)

	game.MovePiece("e5", "d6", "wP")
	_, success := game.PopEvents()

	if !success {
		t.Fatalf("Expected en passant to be valid")
	}
	bbMap, _, _ := game.Bitboards.GenerateMaps()
	if (bbMap[PieceKey{Side: Black, PieceType: Pawn}] & (uint64(1) << 35)) != 0 {
		t.Errorf("Expected black pawn at d5 to be removed")
	}
}

func TestGame_MovePiece_BlackCastling(t *testing.T) {
	bitboards := Bitboards{
		WhiteKings: (uint64(1) << 4),
		BlackRooks: (uint64(1) << 56),
		BlackKings: (uint64(1) << 60),
	}
	game := LoadGame("black-castle", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "KQkq", "-", 0, 1)

	game.MovePiece("e8", "c8", "bK")
	events, success := game.PopEvents()

	if !success {
		t.Fatalf("Expected black castling to be valid")
	}
	
	hasCastle := false
	for _, e := range events {
		if ce, ok := e.(KingCastledEvent); ok {
			hasCastle = true
			if ce.RookFrom != "a8" || ce.RookTo != "d8" {
				t.Errorf("Expected rook move a8->d8, got %s->%s", ce.RookFrom, ce.RookTo)
			}
		}
	}
	if !hasCastle {
		t.Errorf("Expected IsCastling to be true")
	}
}

func TestGame_IsDraw(t *testing.T) {
	bitboards := Bitboards{}
	game := LoadGame("draw-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "draw", "-", "-", 0, 1)

	if !game.IsDraw() {
		t.Errorf("Expected IsDraw to be true for explicit draw result")
	}
}

func TestGame_PawnDoublePush(t *testing.T) {
	bitboardsW := Bitboards{
		WhitePawns: (uint64(1) << 12),
		WhiteKings: (uint64(1) << 4),
		BlackKings: (uint64(1) << 60),
	}
	gameW := LoadGame("pawn-push-w", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboardsW, White, []string{}, "", "KQkq", "-", 0, 1)

	gameW.MovePiece("e2", "e4", "wP")

	if gameW.EnPassantTarget != "e3" {
		t.Errorf("Expected en passant target e3, got %s", gameW.EnPassantTarget)
	}

	bitboardsB := Bitboards{
		BlackPawns: (uint64(1) << 51),
		BlackKings: (uint64(1) << 60),
		WhiteKings: (uint64(1) << 4),
	}
	gameB := LoadGame("pawn-push-b", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboardsB, Black, []string{}, "", "KQkq", "-", 0, 1)

	gameB.MovePiece("d7", "d5", "bP")
	_, successB := gameB.PopEvents()
	if !successB {
		t.Fatalf("Black pawn push failed")
	}
	if gameB.EnPassantTarget != "d6" {
		t.Errorf("Expected en passant target d6, got %s", gameB.EnPassantTarget)
	}
}

func TestGame_AllCastling(t *testing.T) {
	bbW := Bitboards{WhiteKings: (uint64(1) << 4), WhiteRooks: (uint64(1) << 0), BlackKings: (uint64(1) << 60)}
	gW := LoadGame("w-q", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bbW, White, []string{}, "", "Q", "-", 0, 1)
	gW.MovePiece("e1", "c1", "wK")
	eventsW, successW := gW.PopEvents()
	if !successW {
		t.Errorf("White queenside failed")
	}
	hasCastleW := false
	for _, e := range eventsW {
		if ce, ok := e.(KingCastledEvent); ok {
			hasCastleW = true
			if ce.RookFrom != "a1" {
				t.Errorf("White queenside failed")
			}
		}
	}
	if !hasCastleW { t.Errorf("White queenside failed") }

	bbB := Bitboards{BlackKings: (uint64(1) << 60), BlackRooks: (uint64(1) << 63), WhiteKings: (uint64(1) << 4)}
	gB := LoadGame("b-k", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bbB, Black, []string{}, "", "k", "-", 0, 1)
	gB.MovePiece("e8", "g8", "bK")
	eventsB, successB := gB.PopEvents()
	if !successB {
		t.Errorf("Black kingside failed")
	}
	hasCastleB := false
	for _, e := range eventsB {
		if ce, ok := e.(KingCastledEvent); ok {
			hasCastleB = true
			if ce.RookFrom != "h8" {
				t.Errorf("Black kingside failed")
			}
		}
	}
	if !hasCastleB { t.Errorf("Black kingside failed") }
}

func TestNewComputerGame(t *testing.T) {
	format := NewGameFormat("bullet", 1, 0)
	g := NewComputerGame("user-456", "white", format)
	if g.LightPlayer().ID != "user-456" {
		t.Errorf("Expected LightPlayer ID user-456, got %s", g.LightPlayer().ID)
	}
	if g.DarkPlayer().ID != "bot" {
		t.Errorf("Expected DarkPlayer ID bot, got %s", g.DarkPlayer().ID)
	}

	g2 := NewComputerGame("user-456", "black", format)
	if g2.LightPlayer().ID != "bot" {
		t.Errorf("Expected LightPlayer ID bot, got %s", g2.LightPlayer().ID)
	}
	if g2.DarkPlayer().ID != "user-456" {
		t.Errorf("Expected DarkPlayer ID user-456, got %s", g2.DarkPlayer().ID)
	}
}
