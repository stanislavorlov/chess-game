from datetime import datetime
from .game_history import ChessGameHistory
from ..chessboard.file import File
from ..events import (
    GameCreated, GameFinished, GameStarted, KingCastled,
    KingChecked, KingCheckMated, PawnPromoted, PieceCaptured,
    PieceMoveFailed, PieceMoved, SyncedState
)
from ..pieces.piece import Piece
from ..players.players import Players
from ..value_objects.check_state import CheckState
from ..value_objects.game_information import GameInformation
from ..value_objects.game_state import GameState
from ..value_objects.game_status import GameStatus
from ..value_objects.move_failure_reason import MoveFailureReason
from ...domain.chessboard.board import Board
from ...domain.chessboard.position import Position
from ...domain.kernel.aggregate_root import AggregateRoot
from ...domain.movements.movement import Movement
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.side import Side


class ChessGame(AggregateRoot):

    def __init__(self, game_id: ChessGameId, information: GameInformation, players: Players,
                 history: ChessGameHistory):
        super().__init__()
        self._game_id = game_id
        self._players = players
        self._information = information
        # Default starting state
        self._state = GameState(GameStatus.created(), Side.white(), CheckState.default(), Board())
        self._history = history
        
        # Reconstitution: Replay history to reach current state
        if self._history:
            for entry in self._history:
                if entry.history_event:
                    self.apply_event(entry.history_event)

    def emit(self, event):
        self.apply_event(event)
        self.raise_event(event)
        self._history.record(event)

    @staticmethod
    def create(game_id: ChessGameId, players: Players, information: GameInformation):
        instance = ChessGame(
            game_id=game_id,
            information=information,
            players=players,
            history=ChessGameHistory.empty()
        )

        instance.emit(GameCreated(game_id=game_id))
        return instance

    @property
    def game_id(self) -> ChessGameId:
        return self._game_id

    @property
    def players(self) -> Players:
        return self._players

    @property
    def information(self) -> GameInformation:
        return self._information

    @property
    def game_state(self) -> GameState:
        return self._state

    @property
    def history(self) -> ChessGameHistory:
        return self._history

    def get_board(self) -> Board:
        return self._state.board

    def start(self):
        self.emit(GameStarted(game_id=self.game_id, started_date=datetime.now()))
        # Emit initial state for White
        legal_moves = self._state.board.get_legal_moves(self._state.turn)
        self.raise_event(SyncedState(game_id=self.game_id, turn=self._state.turn, legal_moves=legal_moves))

    def finish(self, result: str = ''):
        self.emit(GameFinished(game_id=self.game_id, result=result, finished_date=datetime.now()))

    def apply_event(self, event):
        match event:
            case PieceMoved():
                self._state.board.piece_moved(event)
                # Reset check state when a piece is moved; if there's a new check, a following KingChecked event will set it.
                self._state = GameState(self._state.status, self._state.turn, CheckState.default(), self._state.board)
                self.__switch_turn_from(self._state.turn)
            case PieceCaptured():
                self._state.board.piece_captured(event)
            case GameCreated():
                self._state = GameState(GameStatus.created(), Side.white(), CheckState.default(), self._state.board)
            case GameStarted():
                self._state = GameState(GameStatus.started(), Side.white(), CheckState.default(), self._state.board)
            case GameFinished():
                self._state = GameState(GameStatus.finished(), self._state.turn, self._state.check_state, self._state.board)
            case KingCastled():
                self._state = GameState(self._state.status, self._state.turn, CheckState.default(), self._state.board)
                self._state.board.king_castled(event)
                self.__switch_turn_from(self._state.turn)
            case PawnPromoted():
                self._state.board.pawn_promoted(event)
                self._state = GameState(self._state.status, self._state.turn, CheckState.default(), self._state.board)
                self.__switch_turn_from(self._state.turn)
            case KingChecked() | KingCheckMated():
                self._state = GameState(self._state.status, self._state.turn, CheckState(event.side, event.position), self._state.board)
            case SyncedState():
                # Reconstitution: Sync turn if provided
                side = event.turn
                self._state = GameState(self._state.status, side, self._state.check_state, self._state.board)

    @property
    def black_timer(self):
        return self._information.format.time_remaining.black_time

    @property
    def white_timer(self):
        return self._information.format.time_remaining.white_time

    def timer_tick(self):
        self._information.format.time_remaining.tick(self._state.turn)

        if self._information.format.time_remaining.white_time <= 0:
            self.finish('Time out - Black wins')
        if self._information.format.time_remaining.black_time <= 0:
            self.finish('Time out - White wins')

    @property
    def is_check(self):
        return self._state.board.is_check(self._state.turn)

    @property
    def is_checkmate(self):
        return self._state.board.is_checkmate(self._state.turn)

    def move_piece(self, _from: Position, to: Position, moved: Piece, captured: Piece):
        try:
            # Identify a piece from board
            square = self._state.board[_from]
            piece = square.piece

            if piece is None:
                return

            if not self._state.is_started:
                self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=MoveFailureReason.game_not_started()))
            elif self._state.is_finished:
                self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=MoveFailureReason.game_finished()))
            elif not self._state.turn == piece.get_side():
                self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=MoveFailureReason.not_your_turn()))
            elif piece != moved:
                self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=MoveFailureReason.state_mismatch()))
            else:
                movement = Movement(_from, to)
                legal_moves = self._state.board.get_legal_moves(self._state.turn)

                if movement in legal_moves:
                    # Check for capture
                    target_square = self._state.board[to]
                    if target_square.piece is not None:
                        if target_square.piece != captured:
                            self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=MoveFailureReason.state_mismatch()))
                            return

                        self.emit(PieceCaptured(game_id=self.game_id, from_=_from, to=to, piece=target_square.piece))

                    # Castling side effect: Emit PieceMoved for the Rook
                    if piece.get_piece_type() == PieceType.King and abs(to.file.to_index() - _from.file.to_index()) == 2:
                        is_kingside = to.file.to_index() > _from.file.to_index()
                        rank = _from.rank
                        rook_from_file = File.h() if is_kingside else File.a()
                        rook_to_file = File.f() if is_kingside else File.d()

                        rook_from = Position(rook_from_file, rank)
                        rook_to = Position(rook_to_file, rank)

                        self.emit(KingCastled(
                            game_id=self.game_id,
                            side=piece.get_side(),
                            king_to=to,
                            king_from=_from,
                            rook_to=rook_to,
                            rook_from=rook_from,
                            is_kingside=is_kingside,
                        ))
                    else:
                        self.emit(PieceMoved(game_id=self.game_id, from_=_from, to=to, piece=piece))

                    self.calculate_move_effect()
                else:
                    reason = MoveFailureReason.illegal_move()
                    if piece.get_side() != self._state.turn:
                        reason = MoveFailureReason.not_your_turn()
                    
                    self.raise_event(PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=reason))
        finally:
            legal_moves = self._state.board.get_legal_moves(self._state.turn)
            self.raise_event(SyncedState(game_id=self.game_id, turn=self._state.turn, legal_moves=legal_moves))

    def calculate_move_effect(self):
        side_ = self._state.turn
        king_pos = self._state.board.get_king_position(side_)

        if self.is_checkmate:
            self.emit(KingCheckMated(game_id=self.game_id, side=side_, position=king_pos))
            self.finish('Checkmate')
        elif self.is_check:
            self.emit(KingChecked(game_id=self.game_id, side=side_, position=king_pos))

    def __switch_turn_from(self, turn: Side):
        side = Side.black() if turn == Side.white() else Side.white()
        self._state = GameState(self._state.status, side, self._state.check_state, self._state.board)