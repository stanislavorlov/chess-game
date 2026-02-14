from datetime import datetime
from typing import List, Optional

from ..players.players import Players
from ..value_objects.game_information import GameInformation
from ..value_objects.game_state import GameState
from ..value_objects.game_status import GameStatus
from ...domain.chessboard.board import Board
from ...domain.chessboard.position import Position
from ...domain.events.game_finished import GameFinished
from ...domain.events.game_started import GameStarted
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_moved import PieceMoved
from ...domain.events.piece_move_failed import PieceMoveFailed
from ...domain.kernel.aggregate_root import AggregateRoot
from ...domain.movements.movement import Movement
from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.side import Side
from .game_history import ChessGameHistory


class ChessGame(AggregateRoot):

    def __init__(self, game_id: ChessGameId, information: GameInformation, players: Players,
                 history: ChessGameHistory):
        super().__init__()
        self._game_id = game_id
        self._players = players
        self._information = information
        # Default starting state
        self._state = GameState(GameStatus.created(), Side.white(), Board())
        self._history = history
        
        # Reconstitution: Replay history to reach current state
        if self._history:
            for entry in self._history:
                if entry.history_event:
                    self.apply_event(entry.history_event)

    @staticmethod
    def create(game_id: ChessGameId, players: Players, information: GameInformation):
        instance = ChessGame(
            game_id=game_id,
            information=information,
            players=players,
            history=ChessGameHistory.empty()
        )

        event = GameStarted(game_id=game_id, started_date=datetime.now())
        instance.raise_event(event)
        instance.apply_event(event)
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
        self._state = GameState(GameStatus.started(), self._state.turn, self._state.board)

    def finish(self):
        self._state = GameState(GameStatus.finished(), self._state.turn, self._state.board)

    def apply_event(self, event):
        if isinstance(event, PieceMoved):
            self._state.board.piece_moved(event)
            # Switch turn when piece is moved
            self.__switch_turn_from(self._state.turn)
        elif isinstance(event, PieceCaptured):
            self._state.board.piece_captured(event)
        elif isinstance(event, GameStarted):
            self._state = GameState(GameStatus.started(), Side.white(), self._state.board)
        elif isinstance(event, GameFinished):
            self._state = GameState(GameStatus.finished(), self._state.turn, self._state.board)

    @property
    def black_timer(self):
        return self._information.format.time_remaining.black_time

    @property
    def white_timer(self):
        return self._information.format.time_remaining.white_time

    def timer_tick(self):
        self._information.format.time_remaining.tick(self._state.turn)

        if self._information.format.time_remaining.white_time <= 0:
            self.finish()
        if self._information.format.time_remaining.black_time <= 0:
            self.finish()

    @property
    def is_check(self):
        return self._state.board.is_check(self._state.turn)

    @property
    def is_checkmate(self):
        return self._state.board.is_checkmate(self._state.turn)

    def move_piece(self, _from: Position, to: Position):
        # Identify piece from board
        square = self._state.board[_from]
        piece = square.piece

        if piece is None:
             # This should ideally not happen if client-side validation works
             return

        if not self._state.is_started:
            self.raise_event(
                PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason='Game was not started'))
        elif self._state.is_finished:
            self.raise_event(
                PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason='Game has finished'))
        elif not self._state.turn == piece.get_side():
            self.raise_event(
                PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason="Wait for your turn"))
        elif self.is_check and piece.get_piece_type() != PieceType.King:
            self.raise_event(
                PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason="King is checked"))
        else:
            movement = Movement(_from, to)
            
            # The bitboard engine handles turn validation, pinned pieces, and check evasions
            legal_moves = self._state.board.get_legal_moves(self._state.turn)
            
            print(f'Attempting move: {movement.to_string()}')
            
            if movement in legal_moves:
                # Check for capture
                target_square = self._state.board[to]
                if target_square.piece is not None:
                    capture_event = PieceCaptured(game_id=self.game_id, from_=_from, to=to, piece=target_square.piece)
                    self.raise_event(capture_event)
                    self.apply_event(capture_event)
                    self._history.record(capture_event)

                move_event = PieceMoved(game_id=self.game_id, from_=_from, to=to, piece=piece)
                self.raise_event(move_event)
                self.apply_event(move_event)
                self._history.record(move_event)

                self.calculate_move_effect()
            else:
                reason = "Illegal move"
                if piece.get_side() != self._state.turn:
                    reason = "Wait for your turn"
                
                self.raise_event(
                    PieceMoveFailed(game_id=self.game_id, piece=piece, from_=_from, to=to, reason=reason))

    def calculate_move_effect(self):
        if self.is_checkmate:
            self.raise_event(KingCheckMated(game_id=self.game_id))
            self.raise_event(GameFinished(game_id=self.game_id))
        elif self.is_check:
            self.raise_event(KingChecked(game_id=self.game_id))

    def __switch_turn_from(self, turn: Side):
        side = Side.black() if turn == Side.white() else Side.white()
        self._state = GameState(self._state.status, side, self._state.board)