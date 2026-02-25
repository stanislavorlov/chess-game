from datetime import timedelta
import pandas as pd
from ...domain.kernel.value_object import ValueObject


class TimeFormat(ValueObject):

    def __init__(self, base_time: timedelta, move_increment: timedelta):
        super().__init__()
        self._base_time = base_time
        self._move_increment = move_increment
        self._white = base_time
        self._black = base_time

    @property
    def white_time(self) -> float:
        return self._white.total_seconds()

    @property
    def black_time(self) -> float:
        return self._black.total_seconds()

    def tick(self, side):
        from ...domain.value_objects.side import Side
        if side == Side.white():
            self._white -= timedelta(seconds=1)
        else:
            self._black -= timedelta(seconds=1)

    def consume(self, side, duration: timedelta):
        from ...domain.value_objects.side import Side
        if side == Side.white():
            self._white -= duration
        else:
            self._black -= duration

    def apply_increment(self, side):
        from ...domain.value_objects.side import Side
        if side == Side.white():
            self._white += self._move_increment
        else:
            self._black += self._move_increment

    @property
    def base_time(self):
        return self._base_time

    @property
    def move_increment(self):
        return self._move_increment

    @staticmethod
    def parse_string(base: str, increment: str):
        # Interpret base as minutes and increment as seconds
        base_time = pd.Timedelta(minutes=float(base))
        move_increment = pd.Timedelta(seconds=float(increment))

        time_format = TimeFormat(base_time, move_increment)

        return time_format

    def base_time_string(self):
        return str(self._base_time.total_seconds() / 60)

    def move_increment_string(self):
        return str(self._move_increment.total_seconds())