import unittest
from chessapp.domain.chessboard.board import Board
from chessapp.domain.chessboard.position import Position
from chessapp.domain.chessboard.file import File
from chessapp.domain.chessboard.rank import Rank
from chessapp.domain.pieces.piece_factory import PieceFactory
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.value_objects.side import Side
from chessapp.domain.services.fen_service import FenService

class TestFenService(unittest.TestCase):
    def test_starting_fen(self):
        board = Board()
        # Starting position FEN (no metadata for now)
        expected = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.assertEqual(FenService.generate(board), expected)

    def test_empty_board(self):
        # Create a manually emptied board or a new one and clear it
        board = Board()
        for rank in Rank(1):
            for file in File('a'):
                board._set_piece(Position(file, rank), None)
        
        expected = "8/8/8/8/8/8/8/8"
        self.assertEqual(FenService.generate(board), expected)

    def test_sparse_board(self):
        board = Board()
        # Clear board
        for rank in Rank(1):
            for file in File('a'):
                board._set_piece(Position(file, rank), None)
        
        # Place White King on e1
        board._set_piece(Position.parse("e1"), PieceFactory.create(Side.white(), PieceType.King))
        # Place Black King on e8
        board._set_piece(Position.parse("e8"), PieceFactory.create(Side.black(), PieceType.King))
        # Place White Queen on d4
        board._set_piece(Position.parse("d4"), PieceFactory.create(Side.white(), PieceType.Queen))
        
        # e8=k -> 4k3
        # 7, 6, 5 -> 8
        # d4=Q -> 3Q4
        # 3, 2 -> 8
        # e1=K -> 4K3
        
        expected = "4k3/8/8/8/3Q4/8/8/4K3"
        self.assertEqual(FenService.generate(board), expected)

    def test_multi_empty_squares_merging(self):
        board = Board()
        # Clear board
        for rank in Rank(1):
            for file in File('a'):
                board._set_piece(Position(file, rank), None)
        
        # pieces at a1, c1, e1, g1 (rank 1)
        # a1=R, c1=B, e1=K, g1=B
        board._set_piece(Position.parse("a1"), PieceFactory.create(Side.white(), PieceType.Rook))
        board._set_piece(Position.parse("c1"), PieceFactory.create(Side.white(), PieceType.Bishop))
        board._set_piece(Position.parse("e1"), PieceFactory.create(Side.white(), PieceType.King))
        board._set_piece(Position.parse("g1"), PieceFactory.create(Side.white(), PieceType.Bishop))
        
        # Rank 1: R 1 B 1 K 1 B 1 -> R1B1K1B1
        # Other ranks: 8
        
        expected = "8/8/8/8/8/8/8/R1B1K1B1"
        self.assertEqual(FenService.generate(board), expected)

if __name__ == '__main__':
    unittest.main()
