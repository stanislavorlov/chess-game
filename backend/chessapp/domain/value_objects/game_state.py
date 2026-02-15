from .check_state import CheckState
from ...domain.chessboard.board import Board
from ...domain.kernel.value_object import ValueObject
from ...domain.value_objects.game_status import GameStatus
from ...domain.value_objects.side import Side


class GameState(ValueObject):

    def __init__(self, game_status: GameStatus, turn: Side, check_state: CheckState, board: Board):
        super().__init__()
        self._status = game_status
        self._turn = turn
        self._check_state = check_state
        self._board = board

    @property
    def is_started(self):
        return self._status == GameStatus.started()

    @property
    def is_finished(self):
        return self._status == GameStatus.finished()

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