from datetime import datetime
from typing import Optional, TYPE_CHECKING
from .check_state import CheckState
from ...domain.kernel.value_object import ValueObject
from ...domain.value_objects.game_status import GameStatus
from ...domain.value_objects.side import Side

if TYPE_CHECKING:
    from ...domain.chessboard.board import Board


class GameState(ValueObject):

    def __init__(self, game_status: GameStatus, turn: Side, check_state: CheckState, board: "Board", started_at: Optional[datetime] = None):
        super().__init__()
        self._status = game_status
        self._turn = turn
        self._check_state = check_state
        self._board = board
        self._started_at = started_at

    @property
    def started_at(self) -> Optional[datetime]:
        return self._started_at

    @property
    def is_started(self):
        return self._status.is_following_rank(GameStatus.started())

    @property
    def is_finished(self):
        return self._status.is_following_rank(GameStatus.finished())

    @property
    def turn(self):
        return self._turn

    @property
    def status(self):
        return self._status

    @property
    def board(self):
        return self._board

    @property
    def check_state(self):
        return self._check_state