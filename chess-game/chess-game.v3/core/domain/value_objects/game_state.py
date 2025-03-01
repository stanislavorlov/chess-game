from core.domain.kernel.value_object import ValueObject
from core.domain.value_objects.game_status import GameStatus
from core.domain.value_objects.side import Side


class GameState(ValueObject):

    def __init__(self, game_status: GameStatus, turn: Side):
        super().__init__()
        self._status = game_status
        self._turn = turn

    @property
    def is_started(self):
        return self._status == GameStatus.started()

    @property
    def is_finished(self):
        return self._status == GameStatus.finished()

    @property
    def turn(self):
        return self._turn

    def update_status(self, status: GameStatus):
        if self.is_started() and status == GameStatus.finished():
            self._status = status

    def switch_turn(self):
        self._turn = Side.black() if self._turn == Side.white() else Side.white()