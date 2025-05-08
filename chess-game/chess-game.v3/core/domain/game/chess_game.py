from diator.events import DomainEvent
from core.domain.chessboard.position import Position
from core.domain.events.game_created import GameCreated
from core.domain.events.game_start_failed import GameStartFailed
from core.domain.events.game_started import GameStartedEvent
from core.domain.events.piece_move_failed import PieceMoveFailed
from core.domain.events.piece_moved_completed import PieceMovedCompleted
from core.domain.game.game_history import ChessGameHistory
from core.domain.kernel.aggregate_root import AggregateRoot
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.players.players import Players
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.game_information import GameInformation
from core.domain.value_objects.game_state import GameState
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.side import Side


class ChessGame(AggregateRoot):

    def __init__(self, game_id: ChessGameId, game_info: GameInformation,
                 state: GameState, players: Players, history: ChessGameHistory):
        super().__init__()
        self._id = game_id
        self._info = game_info
        self._state = state
        self._players = players

        self._history = history

    @staticmethod
    def create(game_id: ChessGameId, game_info: GameInformation, players: Players):
        history = ChessGameHistory.empty()
        history.record(GameCreated(game_id=game_id))

        chess_game = ChessGame(game_id, game_info,
                               GameState(GameStatus.created(), Side.white()),
                               players, history)

        chess_game.raise_event(GameCreated(game_id=chess_game.game_id))

        return chess_game

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
            self._state.update_status(GameStatus.started())
            self.raise_event(GameStartedEvent(game_id=self.game_id))

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
        # ToDo: validate King checked, Player Side, Turn
        elif not self._state.turn == piece.get_side():
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason="Piece doesn't belong to player"))
        elif self.is_check and piece.get_piece_type() != PieceType.King:
            self.raise_event(
                PieceMoveFailed(piece=piece, from_=_from, to=to, reason="King is checked"))
        else:
            self.__record_to_history(
                PieceMovedCompleted(game_id=self.game_id,from_=_from,to=to, piece=piece))

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

    def __record_to_history(self, history_record: DomainEvent):
        self._history.record(history_record)