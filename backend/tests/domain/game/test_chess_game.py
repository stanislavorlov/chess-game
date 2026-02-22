import unittest
from datetime import datetime
from chessapp.domain.game.chess_game import ChessGame
from chessapp.domain.value_objects.game_id import ChessGameId
from chessapp.domain.players.players import Players
from chessapp.domain.value_objects.game_information import GameInformation
from chessapp.domain.value_objects.game_format import GameFormat
from chessapp.domain.chessboard.position import Position
from chessapp.domain.chessboard.file import File
from chessapp.domain.chessboard.rank import Rank
from chessapp.domain.value_objects.side import Side
from chessapp.domain.pieces.piece_factory import PieceFactory
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.events.piece_moved import PieceMoved

class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game_id = ChessGameId.generate_id()
        self.players = Players("white_id", "black_id")
        # Need to use specific format that is supported by validation
        game_format = GameFormat.parse_string("rapid", "10m", "0s")
        self.info = GameInformation(game_format, datetime.now(), "Test Game")
        self.game = ChessGame.create(self.game_id, self.players, self.info)
        self.game.start()

    def test_move_enforcement(self):
        # White to move first
        from_pos = Position(File.e(), Rank.r2())
        to_pos = Position(File.e(), Rank.r4())
        piece = self.game.get_board()[from_pos].piece
        
        # valid move
        self.game.move_piece(from_pos, to_pos, piece, None)
        self.assertEqual(self.game.game_state.turn, Side.black())

    def test_calculate_san_pawn(self):
        # 1. e4
        from_pos = Position(File.e(), Rank.r2())
        to_pos = Position(File.e(), Rank.r4())
        piece = self.game.get_board()[from_pos].piece
        
        event = PieceMoved(game_id=self.game_id, from_=from_pos, to=to_pos, piece=piece)
        san = self.game._calculate_san(event, self.game.get_board().clone())
        self.assertEqual(san, "e4")

    def test_calculate_san_knight(self):
        # 1. Nf3
        from_pos = Position(File.g(), Rank.r1())
        to_pos = Position(File.f(), Rank.r3())
        piece = self.game.get_board()[from_pos].piece
        
        event = PieceMoved(game_id=self.game_id, from_=from_pos, to=to_pos, piece=piece)
        san = self.game._calculate_san(event, self.game.get_board().clone())
        self.assertEqual(san, "Nf3")

    def test_calculate_san_capture(self):
        # Setup a capture scenario
        # 1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Bxc6
        
        def make_move(f, t):
            fp = Position.parse(f)
            tp = Position.parse(t)
            p = self.game.get_board()[fp].piece
            target = self.game.get_board()[tp].piece
            self.game.move_piece(fp, tp, p, target)

        make_move("e2", "e4")
        make_move("e7", "e5")
        make_move("g1", "f3")
        make_move("b8", "c6")
        make_move("f1", "b5")
        make_move("a7", "a6")
        
        # Now Bxc6
        from_pos = Position.parse("b5")
        to_pos = Position.parse("c6")
        piece = self.game.get_board()[from_pos].piece
        board_before = self.game.get_board().clone()
        
        event = PieceMoved(game_id=self.game_id, from_=from_pos, to=to_pos, piece=piece)
        san = self.game._calculate_san(event, board_before)
        self.assertEqual(san, "Bxc6")

    def test_moves_count(self):
        # Initial moves count is 0
        self.assertEqual(self.game.history.moves_count(), 0)
        
        # Make a move
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        piece = self.game.get_board()[from_pos].piece
        self.game.move_piece(from_pos, to_pos, piece, None)
        
        # Moves count should be 1
        self.assertEqual(self.game.history.moves_count(), 1)
        
        # Emit a non-move event (e.g. KingChecked)
        from chessapp.domain.events.king_checked import KingChecked
        self.game.history.record(KingChecked(game_id=self.game_id, side=Side.black(), position=Position.parse("e8")), "Check")
        
        # Moves count should still be 1 (PieceMoved only)
        self.assertEqual(self.game.history.moves_count(), 1)
        # Total history: GameCreated, GameStarted, PieceMoved, KingChecked (manual)
        self.assertEqual(self.game.history.count(), 4)

if __name__ == '__main__':
    unittest.main()
