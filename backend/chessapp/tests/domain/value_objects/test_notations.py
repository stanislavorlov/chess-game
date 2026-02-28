import unittest
from chessapp.domain.chessboard.position import Position
from chessapp.domain.chessboard.file import File
from chessapp.domain.chessboard.rank import Rank
from chessapp.domain.value_objects.uci import UCI
from chessapp.domain.value_objects.san import SAN
from chessapp.domain.chessboard.board import Board
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.pieces.pawn import Pawn
from chessapp.domain.value_objects.side import Side

class TestMoveNotations(unittest.TestCase):
    def test_uci_formatting(self):
        f = Position(File.e(), Rank.r2())
        t = Position(File.e(), Rank.r4())
        uci = UCI.from_positions(f, t)
        self.assertEqual(str(uci), "e2e4")

    def test_san_pawn_move(self):
        board = Board()
        f = Position(File.e(), Rank.r2())
        t = Position(File.e(), Rank.r4())
        pawn = Pawn(Side.white())
        event = PieceMoved(game_id=None, from_=f, to=t, piece=pawn)
        
        san = SAN.from_move(event, board)
        self.assertEqual(str(san), "e4")

    def test_san_capture(self):
        board = Board()
        # Setup a capture scenario
        # White Pawn at e4, Black Pawn at d5
        from chessapp.domain.pieces.pawn import Pawn
        wp = Pawn(Side.white())
        bp = Pawn(Side.black())
        
        board._set_piece(Position(File.e(), Rank.r4()), wp)
        board._set_piece(Position(File.d(), Rank.r5()), bp)
        
        event = PieceMoved(game_id=None, from_=Position(File.e(), Rank.r4()), to=Position(File.d(), Rank.r5()), piece=wp)
        san = SAN.from_move(event, board)
        # Note: SAN logic in Value Object follows simple capture representation for now
        self.assertEqual(str(san), "exd5")

if __name__ == '__main__':
    unittest.main()
