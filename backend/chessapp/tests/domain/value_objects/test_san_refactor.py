import unittest
from unittest.mock import MagicMock
from chessapp.domain.value_objects.san import SAN

class TestSanRefactor(unittest.TestCase):
    def test_from_move_raises_value_error_for_invalid_event(self):
        invalid_event = MagicMock()
        board = MagicMock()
        
        with self.assertRaises(ValueError) as cm:
            SAN.from_move(invalid_event, board)
        
        self.assertIn("Unsupported event type", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
