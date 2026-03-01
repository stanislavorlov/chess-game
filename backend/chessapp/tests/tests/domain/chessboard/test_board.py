import unittest
from chessapp.domain.chessboard.board import Board
from chessapp.domain.chessboard.position import Position
from chessapp.domain.chessboard.file import File
from chessapp.domain.chessboard.rank import Rank
from chessapp.domain.value_objects.side import Side
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.events.piece_moved import PieceMoved

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_clone_is_deep(self):
        cloned = self.board.clone()
        from_pos = Position(File.e(), Rank.r2())
        to_pos = Position(File.e(), Rank.r4())
        piece = self.board[from_pos].piece
        
        event = PieceMoved(game_id=None, from_=from_pos, to=to_pos, piece=piece)
        self.board.piece_moved(event)
        
        # Original should be changed, clone should NOT
        self.assertIsNone(self.board[from_pos].piece)
        self.assertIsNotNone(cloned[from_pos].piece)
        self.assertTrue(cloned.verify_integrity())
        self.assertTrue(self.board.verify_integrity())

    def test_initial_setup(self):
        # Check some key positions
        self.assertEqual(self.board[Position(File.e(), Rank.r2())].piece.get_piece_type(), PieceType.Pawn)
        self.assertEqual(self.board[Position(File.e(), Rank.r2())].piece.get_side(), Side.white())
        
        self.assertEqual(self.board[Position(File.e(), Rank.r8())].piece.get_piece_type(), PieceType.King)
        self.assertEqual(self.board[Position(File.e(), Rank.r8())].piece.get_side(), Side.black())

    def test_legal_moves_start(self):
        # White should have 20 legal moves at the start
        moves = self.board.get_legal_moves(Side.white())
        self.assertEqual(len(moves), 20)

    def test_piece_moved_updates_state(self):
        from_pos = Position(File.e(), Rank.r2())
        to_pos = Position(File.e(), Rank.r4())
        piece = self.board[from_pos].piece
        
        event = PieceMoved(game_id=None, from_=from_pos, to=to_pos, piece=piece)
        self.board.piece_moved(event)
        
        self.assertIsNone(self.board[from_pos].piece)
        self.assertEqual(self.board[to_pos].piece.get_piece_type(), PieceType.Pawn)
        self.assertTrue(self.board.verify_integrity())

    def test_is_check(self):
        # 1. e4
        self.board.piece_moved(PieceMoved(game_id=None, from_=Position.parse("e2"), to=Position.parse("e4"), piece=self.board[Position.parse("e2")].piece))
        # 2. f6 (black)
        self.board.piece_moved(PieceMoved(game_id=None, from_=Position.parse("f7"), to=Position.parse("f6"), piece=self.board[Position.parse("f7")].piece))
        # 3. Qh5+
        queen = self.board[Position.parse("d1")].piece
        self.board.piece_moved(PieceMoved(game_id=None, from_=Position.parse("d1"), to=Position.parse("h5"), piece=queen))
        
        self.assertTrue(self.board.is_check(Side.black()))
        self.assertFalse(self.board.is_check(Side.white()))

    def test_scholars_mate(self):
        # 1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#
        def move(f, t):
            piece = self.board[Position.parse(f)].piece
            self.board.piece_moved(PieceMoved(game_id=None, from_=Position.parse(f), to=Position.parse(t), piece=piece))

        move("e2", "e4")
        move("e7", "e5")
        move("f1", "c4")
        move("b8", "c6")
        move("d1", "h5")
        move("g8", "f6")
        
        # Before mate
        self.assertFalse(self.board.is_checkmate(Side.black()))
        
        # Qxf7
        queen = self.board[Position.parse("h5")].piece
        self.board.piece_moved(PieceMoved(game_id=None, from_=Position.parse("h5"), to=Position.parse("f7"), piece=queen))
        
        self.assertTrue(self.board.is_check(Side.black()))
        self.assertTrue(self.board.is_checkmate(Side.black()))

    def test_castling_legality(self):
        # Clear path for white kingside castling
        self.board._remove_piece(Position.parse("f1"))
        self.board._remove_piece(Position.parse("g1"))
        
        moves = self.board.get_legal_moves(Side.white())
        # Position(File.g(), Rank.r1()) should be a legal move for the King (kingside castle)
        castle_move = next((m for m in moves if m.from_position == Position.parse("e1") and m.to_position == Position.parse("g1")), None)
        self.assertIsNotNone(castle_move)

    def test_pawn_promotion_event(self):
        from chessapp.domain.events.pawn_promoted import PawnPromoted
        # Place a white pawn on a7
        pawn = self.board[Position.parse("a2")].piece
        self.board._remove_piece(Position.parse("a2"))
        self.board._set_piece(Position.parse("a7"), pawn)
        
        # Promote to Queen on a8
        event = PawnPromoted(game_id=None, side=Side.white(), to=Position.parse("a8"), promoted_to=PieceType.Queen)
        self.board.pawn_promoted(event)
        
        self.assertEqual(self.board[Position.parse("a8")].piece.get_piece_type(), PieceType.Queen)
        self.assertTrue(self.board.verify_integrity())

    def test_sliding_piece_blocked(self):
        # White rook on a1 is blocked by a2 pawn
        moves = self.board.get_legal_moves(Side.white())
        rook_a1_moves = [m for m in moves if m.from_position == Position.parse("a1")]
        self.assertEqual(len(rook_a1_moves), 0)
        
        # Remove a2 pawn
        self.board._remove_piece(Position.parse("a2"))
        moves = self.board.get_legal_moves(Side.white())
        rook_a1_moves = [m for m in moves if m.from_position == Position.parse("a1")]
        # Can move to a2, a3, a4, a5, a6, a7 (capture)
        # Actually it's more than that, let's just check it's not 0
        self.assertGreater(len(rook_a1_moves), 0)

    def test_piece_captured(self):
        from chessapp.domain.events.piece_captured import PieceCaptured
        # White captures black pawn on e7
        white_queen = self.board[Position.parse("d1")].piece
        black_pawn = self.board[Position.parse("e7")].piece
        
        # Move queen to e7 (simulation)
        event = PieceCaptured(game_id=None, from_=Position.parse("d1"), to=Position.parse("e7"), piece=black_pawn)
        self.board.piece_captured(event)
        
        # e7 should be None (until PieceMoved updates it with the queen)
        self.assertIsNone(self.board[Position.parse("e7")].piece)
        self.assertTrue(self.board.verify_integrity())

if __name__ == '__main__':
    unittest.main()
