package models

import (
	"engineapp/handlers/ws"
	"testing"
)

func TestGame_MovePiece_Basic(t *testing.T) {
	// Setup standard game
	bitboards := Bitboards{
		WhitePawns: 0x000000000000FF00,
		WhiteRooks: 0x0000000000000081,
		WhiteKings: 0x0000000000000010,
		BlackPawns: 0x00FF000000000000,
		BlackKings: 0x1000000000000000,
	}
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	// Move e2 to e4
	move := ws.GameRequest{
		From: "e2",
		To:   "e4",
		Piece: ws.Piece{PieceType: "wP", Side: ws.Side{Value: "w"}},
	}
	result := game.MovePiece(move)

	if !result.Valid {
		t.Errorf("Expected move e2e4 to be valid, got error: %s", result.Error)
	}
	if game.Turn() != "w" { // Wait! Turn toggles! White moved, now it's black.
		// Wait, game.Turn() returns "w" or "b".
		// In my LoadGame, I set turn to White.
		// After MovePiece, it should be Black.
	}
	if game.Turn() != "b" {
		t.Errorf("Expected turn to be black after white move, got %s", game.Turn())
	}
}

func TestGame_MovePiece_Castling(t *testing.T) {
	// Setup game ready for white kingside castling
	bitboards := Bitboards{
		WhiteRooks: 0x0000000000000081,
		WhiteKings: 0x0000000000000010,
		BlackKings: 0x1000000000000000,
	}
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	// Castle kingside (e1 to g1)
	move := ws.GameRequest{
		From: "e1",
		To:   "g1",
		Piece: ws.Piece{PieceType: "wK", Side: ws.Side{Value: "w"}},
	}
	result := game.MovePiece(move)

	if !result.Valid {
		t.Fatalf("Expected castling to be valid, got error: %s", result.Error)
	}
	if !result.IsCastling {
		t.Errorf("Expected IsCastling to be true")
	}
	if result.CastlingRookFrom != "h1" || result.CastlingRookTo != "f1" {
		t.Errorf("Expected rook move h1->f1, got %s->%s", result.CastlingRookFrom, result.CastlingRookTo)
	}

	// Verify castling rights updated
	if game.CastlingRights == "KQkq" || game.CastlingRights == "Kkq" {
		t.Errorf("Expected white castling rights to be removed, got %s", game.CastlingRights)
	}
}

func TestGame_IsCheck(t *testing.T) {
	// Setup game where black king is in check by white rook
	bitboards := Bitboards{
		WhiteRooks: 0x0000000000000008, // Rook at d1
		WhiteKings: 0x0000000000000001, // King at a1
		BlackKings: 0x0800000000000000, // King at d8
	}
	// It's black's turn
	game := LoadGame("test-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "-", "-", 0, 1)

	if !game.IsCheck() {
		t.Errorf("Expected black king to be in check")
	}
}

func TestGame_IsCheckmate(t *testing.T) {
	// Setup a simple back-rank mate
	bitboards := Bitboards{
		WhiteRooks: (uint64(1) << 56) | (uint64(1) << 48), // a8 and a7
		BlackKings: (uint64(1) << 63), // h8
		WhiteKings: (uint64(1) << 0),  // a1
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
	// Setup a classic stalemate position
	// Black King at a8 (56), White Queen at c7 (50), White King at a1 (0)
	bitboards := Bitboards{
		WhiteKings:  (uint64(1) << 0),  // a1
		WhiteQueens: (uint64(1) << 50), // c7
		BlackKings:  (uint64(1) << 56), // a8
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
		WhiteKings: (uint64(1) << 4),  // e1
		BlackKings: (uint64(1) << 60), // e8
	}
	game := LoadGame("fen-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "KQkq", "-", 0, 1)

	expectedStart := "4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1"
	if game.FEN() != expectedStart {
		t.Errorf("Expected FEN %s, got %s", expectedStart, game.FEN())
	}
}

func TestGame_MovePiece_Capture(t *testing.T) {
	bitboards := Bitboards{
		WhiteRooks: (uint64(1) << 0),  // a1
		WhiteKings: (uint64(1) << 4),  // e1
		BlackPawns: (uint64(1) << 56), // a8
		BlackKings: (uint64(1) << 60), // e8
	}
	game := LoadGame("capture-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{}, "", "-", "-", 0, 1)

	// White Rook captures Black Pawn on a8
	move := ws.GameRequest{
		From: "a1",
		To:   "a8",
		Piece: ws.Piece{PieceType: "wR", Side: ws.Side{Value: "w"}},
	}
	result := game.MovePiece(move)

	if !result.Valid {
		t.Fatalf("Expected capture to be valid, got: %s", result.Error)
	}
	if !result.IsCapture {
		t.Errorf("Expected IsCapture to be true")
	}
	if result.CapturedPiece != "bP" {
		t.Errorf("Expected captured piece bP, got %s", result.CapturedPiece)
	}
}

func TestGame_MovePiece_EnPassant(t *testing.T) {
	// White pawn at e5, Black pawn at d5 (just moved from d7)
	bitboards := Bitboards{
		WhitePawns: (uint64(1) << 36), // e5
		WhiteKings: (uint64(1) << 4),  // e1
		BlackPawns: (uint64(1) << 35), // d5
		BlackKings: (uint64(1) << 60), // e8
	}
	// En passant target is d6
	game := LoadGame("ep-game", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, White, []string{"d7d5"}, "", "-", "d6", 0, 1)

	move := ws.GameRequest{
		From: "e5",
		To:   "d6",
		Piece: ws.Piece{PieceType: "wP", Side: ws.Side{Value: "w"}},
	}
	result := game.MovePiece(move)

	if !result.Valid {
		t.Fatalf("Expected en passant to be valid, got: %s", result.Error)
	}
	// Verify black pawn at d5 is gone
	bbMap, _, _ := game.Bitboards.GenerateMaps()
	if (bbMap[PieceKey{Side: Black, PieceType: Pawn}] & (uint64(1) << 35)) != 0 {
		t.Errorf("Expected black pawn at d5 to be removed")
	}
}

func TestGame_MovePiece_BlackCastling(t *testing.T) {
	bitboards := Bitboards{
		WhiteKings: (uint64(1) << 4),  // e1
		BlackRooks: (uint64(1) << 56), // a8
		BlackKings: (uint64(1) << 60), // e8
	}
	game := LoadGame("black-castle", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboards, Black, []string{}, "", "KQkq", "-", 0, 1)

	// Black Queen-side castling (e8 to c8)
	move := ws.GameRequest{
		From: "e8",
		To:   "c8",
		Piece: ws.Piece{PieceType: "bK", Side: ws.Side{Value: "b"}},
	}
	result := game.MovePiece(move)

	if !result.Valid {
		t.Fatalf("Expected black castling to be valid, got: %s", result.Error)
	}
	if !result.IsCastling {
		t.Errorf("Expected IsCastling to be true")
	}
	if result.CastlingRookFrom != "a8" || result.CastlingRookTo != "d8" {
		t.Errorf("Expected rook move a8->d8, got %s->%s", result.CastlingRookFrom, result.CastlingRookTo)
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
	// White pawn at e2
	bitboardsW := Bitboards{
		WhitePawns: (uint64(1) << 12),
		WhiteKings: (uint64(1) << 4),
		BlackKings: (uint64(1) << 60),
	}
	gameW := LoadGame("pawn-push-w", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboardsW, White, []string{}, "", "KQkq", "-", 0, 1)

	moveW := ws.GameRequest{
		From: "e2", To: "e4",
		Piece: ws.Piece{PieceType: "wP", Side: ws.Side{Value: "w"}},
	}
	gameW.MovePiece(moveW)

	if gameW.EnPassantTarget != "e3" {
		t.Errorf("Expected en passant target e3, got %s", gameW.EnPassantTarget)
	}

	// Black pawn at d7
	bitboardsB := Bitboards{
		BlackPawns: (uint64(1) << 51),
		BlackKings: (uint64(1) << 60),
		WhiteKings: (uint64(1) << 4),
	}
	gameB := LoadGame("pawn-push-b", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bitboardsB, Black, []string{}, "", "KQkq", "-", 0, 1)

	moveB := ws.GameRequest{
		From: "d7", To: "d5",
		Piece: ws.Piece{PieceType: "bP", Side: ws.Side{Value: "b"}},
	}
	resB := gameB.MovePiece(moveB)
	if !resB.Valid {
		t.Fatalf("Black pawn push failed: %s", resB.Error)
	}
	if gameB.EnPassantTarget != "d6" {
		t.Errorf("Expected en passant target d6, got %s", gameB.EnPassantTarget)
	}
}

func TestGame_AllCastling(t *testing.T) {
	// White Queenside
	bbW := Bitboards{WhiteKings: (uint64(1) << 4), WhiteRooks: (uint64(1) << 0), BlackKings: (uint64(1) << 60)}
	gW := LoadGame("w-q", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bbW, White, []string{}, "", "Q", "-", 0, 1)
	resW := gW.MovePiece(ws.GameRequest{From: "e1", To: "c1", Piece: ws.Piece{PieceType: "wK", Side: ws.Side{Value: "w"}}})
	if !resW.IsCastling || resW.CastlingRookFrom != "a1" {
		t.Errorf("White queenside failed")
	}

	// Black Kingside
	bbB := Bitboards{BlackKings: (uint64(1) << 60), BlackRooks: (uint64(1) << 63), WhiteKings: (uint64(1) << 4)}
	gB := LoadGame("b-k", Started, Bullet_1_0, "standard", NewAuthenticatedPlayer("p1"), NewAuthenticatedPlayer("p2"), bbB, Black, []string{}, "", "k", "-", 0, 1)
	resB := gB.MovePiece(ws.GameRequest{From: "e8", To: "g8", Piece: ws.Piece{PieceType: "bK", Side: ws.Side{Value: "b"}}})
	if !resB.IsCastling || resB.CastlingRookFrom != "h8" {
		t.Errorf("Black kingside failed")
	}
}
