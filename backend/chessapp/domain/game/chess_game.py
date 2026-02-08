from datetime import datetime
from ...domain.chessboard.board import Board
from ...domain.chessboard.position import Position
from ...domain.events.game_created import GameCreated
from ...domain.events.game_start_failed import GameStartFailed
from ...domain.events.game_started import GameStarted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_move_failed import PieceMoveFailed
from ...domain.events.piece_moved import PieceMoved
from ...domain.game.game_history import ChessGameHistory
from ...domain.kernel.aggregate_root import AggregateRoot
from ...domain.kernel.base import BaseEvent
from ...domain.movements.movement import Movement
from ...domain.movements.movement_intent_factory import MovementIntentFactory
from ...domain.movements.movement_specification import MovementSpecification
from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.players.players import Players
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.game_information import GameInformation
from ...domain.value_objects.game_state import GameState
from ...domain.value_objects.game_status import GameStatus
from ...domain.value_objects.side import Side


class ChessGame(AggregateRoot):

    def __init__(self, game_id: ChessGameId, game_info: GameInformation,
                players: Players, history: ChessGameHistory):
        super().__init__()
        self._id = game_id
        self._info = game_info
        self._players = players
        self._history = history
        self._state = GameState(GameStatus.created(), Side.white(), Board())

        for history_entry in self._history:
            self.apply_event(history_entry.history_event)

    @staticmethod
    def create(game_id: ChessGameId, game_info: GameInformation, players: Players):
        chess_game = ChessGame(game_id, game_info,
                               players, ChessGameHistory.empty())

        chess_game.raise_event(GameCreated(game_id=chess_game.game_id))

        return chess_game

    def apply_event(self, domain_event: BaseEvent):
        match domain_event:
            case GameCreated():
                self._state = GameState(GameStatus.created(), Side.white(), Board())
            case GameStarted():
                self._state = GameState(GameStatus.started(), Side.white(), self._state.board)
            case PieceMoved() as event:
                board = self._state.board
                board.piece_moved(event)
                self.__switch_turn_from(self._state.turn)
            case PieceCaptured() as event:
                board = self._state.board
                board.piece_captured(event)

    def get_board(self):
        return self._state.board

    @property
    def information(self):
        return self._info

    @property
    def game_id(self):
        return self._id

    @property
    def game_state(self):
        return self._state

    @property
    def players(self):
        return self._players

    @property
    def history(self):
        return self._history

    def start(self):
        if self._state.is_started:
            self.raise_event(GameStartFailed(game_id=self.game_id))

            return
        else:
            self._state = GameState(GameStatus.started(), self._state.turn, self._state.board)
            self.raise_event(GameStarted(game_id=self.game_id, started_date=datetime.now()))

            return

    @property
    def is_check(self):
        # ToDo: retrieve latest event from History (KingChecked)
        return False

    @property
    def is_checkmate(self):
        # ToDo: retrieve latest event from History (KingChecked)
        return False

    def move_piece(self, piece: Piece, _from: Position, to: Position):
        if not self._state.is_started:
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason='Game was not started'))
        elif self._state.is_finished:
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason='Game has finished'))
        elif not self._state.turn == piece.get_side():
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason="Piece doesn't belong to player"))
        elif self.is_check and piece.get_piece_type() != PieceType.King:
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason="King is checked"))
        else:
            movement = Movement(piece, _from, to)
            movement_specification = MovementSpecification(piece.get_rule())
            movement_intent = MovementIntentFactory.create(movement)

            if movement_specification.is_satisfied_by(movement_intent):
                self.raise_event(
                    PieceMoved(game_id=self.game_id, from_=_from, to=to, piece=piece))

                self.__switch_turn_from(self._state.turn)
            else:
                self.raise_event(
                    PieceMoveFailed(piece=piece, from_=_from, to=to, reason="Illegal move for this piece"))

        self.calculate_move_effect()

    def calculate_move_effect(self):
        pass
        # promotion happened
        # piece captured
        # king checked
        # checkmate
        # stalemate
        # castling

        # publish event

    def promote_pawn(self):
        pass

    def raise_event(self, domain_event: BaseEvent):
        self.__record_to_history(domain_event)

        super().raise_event(domain_event)

    def __switch_turn_from(self, turn: Side):
        side = Side.black() if turn == Side.white() else Side.white()

        self._state = GameState(self._state.status, side, self._state.board)

    def __record_to_history(self, history_record: BaseEvent):
        self._history.record(history_record)