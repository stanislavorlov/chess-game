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
from chessapp.domain.value_objects.game_status import GameStatus
from chessapp.domain.events.piece_moved import PieceMoved
from chessapp.domain.events.piece_captured import PieceCaptured
from chessapp.domain.events.game_created import GameCreated
from chessapp.domain.events.game_started import GameStarted
from chessapp.domain.events.game_finished import GameFinished
from chessapp.domain.events.king_castled import KingCastled
from chessapp.domain.events.pawn_promoted import PawnPromoted
from chessapp.domain.events.king_checked import KingChecked
from chessapp.domain.events.king_checkmated import KingCheckMated
from chessapp.domain.events.synced_state import SyncedState
from chessapp.domain.events.piece_move_failed import PieceMoveFailed
from chessapp.domain.value_objects.move_failure_reason import MoveFailureReason

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

    def test_apply_event_game_created(self):
        event = GameCreated(game_id=self.game_id)
        self.game.apply_event(event)
        self.assertEqual(self.game.game_state.status, GameStatus.created())
        self.assertEqual(self.game.game_state.turn, Side.white())

    def test_apply_event_game_started(self):
        event = GameStarted(game_id=self.game_id, started_date=datetime.now())
        self.game.apply_event(event)
        self.assertEqual(self.game.game_state.status, GameStatus.started())

    def test_apply_event_game_finished(self):
        event = GameFinished(game_id=self.game_id, result="Resignation", finished_date=datetime.now())
        self.game.apply_event(event)
        self.assertEqual(self.game.game_state.status, GameStatus.finished())

    def test_apply_event_piece_moved(self):
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        piece = self.game.get_board()[from_pos].piece
        event = PieceMoved(game_id=self.game_id, from_=from_pos, to=to_pos, piece=piece)
        
        self.game.apply_event(event)
        self.assertIsNone(self.game.get_board()[from_pos].piece)
        self.assertEqual(self.game.get_board()[to_pos].piece, piece)

    def test_apply_event_piece_captured(self):
        from_pos = Position.parse("d2")
        to_pos = Position.parse("d4")
        pawn = self.game.get_board()[from_pos].piece
        event = PieceCaptured(game_id=self.game_id, from_=from_pos, to=to_pos, piece=pawn)
        self.game.apply_event(event)
        self.assertIsNone(self.game.get_board()[to_pos].piece)

    def test_apply_event_king_castled(self):
        # Setup castling event manually
        king_from = Position.parse("e1")
        king_to = Position.parse("g1")
        rook_from = Position.parse("h1")
        rook_to = Position.parse("f1")
        
        event = KingCastled(
            game_id=self.game_id,
            side=Side.white(),
            king_from=king_from,
            king_to=king_to,
            rook_from=rook_from,
            rook_to=rook_to,
            is_kingside=True
        )
        
        self.game.apply_event(event)
        
        # Verify King and Rook moved
        self.assertEqual(self.game.get_board()[king_to].piece.get_piece_type(), PieceType.King)
        self.assertEqual(self.game.get_board()[rook_to].piece.get_piece_type(), PieceType.Rook)
        self.assertIsNone(self.game.get_board()[king_from].piece)
        self.assertIsNone(self.game.get_board()[rook_from].piece)

    def test_apply_event_pawn_promoted(self):
         # Place a pawn on a7 manually for simulation if needed, but apply_event just sets it
        to_pos = Position.parse("a8")
        event = PawnPromoted(game_id=self.game_id, side=Side.white(), to=to_pos, promoted_to=PieceType.Queen)
        self.game.apply_event(event)
        
        self.assertEqual(self.game.get_board()[to_pos].piece.get_piece_type(), PieceType.Queen)
        self.assertEqual(self.game.get_board()[to_pos].piece.get_side(), Side.white())

    def test_apply_event_king_checked(self):
        event = KingChecked(game_id=self.game_id, side=Side.black(), position=Position.parse("e8"))
        self.game.apply_event(event)
        self.assertEqual(self.game.game_state.check_state.side_checked, Side.black())

    def test_apply_event_king_checkmated(self):
        event = KingCheckMated(game_id=self.game_id, side=Side.white(), position=Position.parse("e1"))
        self.game.apply_event(event)
        # Check if it marks something? Actually apply_event for KingCheckMated might not do anything specific to state yet
        # depends on implementation. But we test it executes.
        pass

    def test_apply_event_synced_state(self):
        event = SyncedState(game_id=self.game_id, turn=Side.black(), legal_moves=[])
        self.game.apply_event(event)
        self.assertEqual(self.game.game_state.turn, Side.black())

    def test_move_piece_guard_not_started(self):
        game2 = ChessGame.create(self.game_id, self.players, self.info)
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        piece2 = game2.get_board()[from_pos].piece
        game2.move_piece(from_pos, to_pos, piece2, None)
        failed_event = next(e for e in game2.domain_events if isinstance(e, PieceMoveFailed))
        self.assertEqual(failed_event.reason.code, "GAME_NOT_STARTED")

    def test_move_piece_guard_finished(self):
        self.game.finish("Draw")
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        piece = self.game.get_board()[from_pos].piece
        self.game.move_piece(from_pos, to_pos, piece, None)
        failed_event = [e for e in self.game.domain_events if isinstance(e, PieceMoveFailed)][-1]
        self.assertEqual(failed_event.reason.code, "GAME_FINISHED")

    def test_move_piece_guard_not_your_turn(self):
        black_from = Position.parse("e7")
        black_to = Position.parse("e5")
        black_piece = self.game.get_board()[black_from].piece
        self.game.move_piece(black_from, black_to, black_piece, None)
        failed_event = [e for e in self.game.domain_events if isinstance(e, PieceMoveFailed)][-1]
        self.assertEqual(failed_event.reason.code, "NOT_YOUR_TURN")

    def test_move_piece_guard_piece_mismatch(self):
        from_pos = Position.parse("e2")
        to_pos = Position.parse("e4")
        wrong_piece = PieceFactory.create(PieceType.Rook, Side.white())
        self.game.move_piece(from_pos, to_pos, wrong_piece, None)
        failed_event = [e for e in self.game.domain_events if isinstance(e, PieceMoveFailed)][-1]
        self.assertEqual(failed_event.reason.code, "STATE_MISMATCH")

    def test_move_piece_guard_illegal_move(self):
        from_pos = Position.parse("e2")
        illegal_to = Position.parse("e1")
        piece = self.game.get_board()[from_pos].piece
        self.game.move_piece(from_pos, illegal_to, piece, None)
        failed_event = [e for e in self.game.domain_events if isinstance(e, PieceMoveFailed)][-1]
        self.assertEqual(failed_event.reason.code, "ILLEGAL_MOVE")

    def test_move_piece_success_and_effects(self):
        # 1. Capture success
        # Setup: e4 d5
        self.game.move_piece(Position.parse("e2"), Position.parse("e4"), self.game.get_board()[Position.parse("e2")].piece, None)
        self.game.move_piece(Position.parse("d7"), Position.parse("d5"), self.game.get_board()[Position.parse("d7")].piece, None)
        
        # exd5
        white_pawn = self.game.get_board()[Position.parse("e4")].piece
        black_pawn = self.game.get_board()[Position.parse("d5")].piece
        self.game.move_piece(Position.parse("e4"), Position.parse("d5"), white_pawn, black_pawn)
        
        self.assertTrue(any(isinstance(e, PieceCaptured) for e in self.game.domain_events))
        self.assertEqual(self.game.get_board()[Position.parse("d5")].piece, white_pawn)
        
        # 2. Checkmate effect
        # Scholar's mate: 1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7#
        self.setUp()
        def move(f, t):
            fp = Position.parse(f)
            tp = Position.parse(t)
            p = self.game.get_board()[fp].piece
            target = self.game.get_board()[tp].piece
            self.game.move_piece(fp, tp, p, target)

        move("e2", "e4") # 1. e4
        move("e7", "e5") # 1... e5
        move("f1", "c4") # 2. Bc4
        move("b8", "c6") # 2... Nc6
        move("d1", "h5") # 3. Qh5
        move("g8", "f6") # 3... Nf6
        
        # 4. Qxf7#
        q_from = Position.parse("h5")
        q_to = Position.parse("f7")
        queen = self.game.get_board()[q_from].piece
        target = self.game.get_board()[q_to].piece
        
        self.game.move_piece(q_from, q_to, queen, target)
        
        self.assertTrue(self.game.game_state.is_finished)
        self.assertTrue(any(isinstance(e, KingCheckMated) for e in self.game.domain_events))
        self.assertEqual(self.game.game_state.status, GameStatus.finished())

if __name__ == '__main__':
    unittest.main()
