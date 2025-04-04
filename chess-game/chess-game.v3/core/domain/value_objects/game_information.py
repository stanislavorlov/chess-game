from datetime import datetime
from core.domain.kernel.value_object import ValueObject
from core.domain.value_objects.game_format import GameFormat


class GameInformation(ValueObject):

    def __init__(self, game_format: GameFormat, game_date: datetime, name: str):
        super().__init__()
        self._date = game_date
        self._name = name
        self._game_format = game_format

    @property
    def date(self):
        return self._date

    @property
    def name(self):
        return self._name

    @property
    def format(self):
        return self._game_format