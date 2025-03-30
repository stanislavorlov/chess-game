from datetime import datetime
from core.domain.kernel.value_object import ValueObject


class GameInformation(ValueObject):

    def __init__(self, moves_counter: int, game_date: datetime, name: str):
        super().__init__()
        self._moves_counter = moves_counter
        self._date = game_date
        self._name = name

    @property
    def count_of_moves(self):
        return self._moves_counter

    @property
    def date(self):
        return self._date

    @property
    def name(self):
        return self._name