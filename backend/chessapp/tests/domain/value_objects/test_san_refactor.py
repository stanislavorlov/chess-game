import unittest
from chessapp.domain.chessboard.board import Board
from chessapp.domain.services.san_service import SanService


class TestSanRefactor(unittest.TestCase):
    def test_from_move_raises_value_error_for_invalid_event(self):
        board = Board()
        invalid_event = object()
        with self.assertRaises(ValueError) as cm:
            SanService.calculate(invalid_event, board)
        
        self.assertIn("Unsupported event type", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
