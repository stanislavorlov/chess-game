from core.domain.kernel.value_object import ValueObject
from core.domain.value_objects.game_format import GameFormat


class GameSettings(ValueObject):

    def __init__(self, game_format: GameFormat):
        super().__init__()
        self._game_format = game_format

    @property
    def format(self):
        return self._game_format