import re
from datetime import timedelta

from core.domain.kernel.value_object import ValueObject


class GameFormat(ValueObject):

    def __init__(self, time_remaining: timedelta):
        super().__init__()
        self._time_remaining = time_remaining

    @staticmethod
    def rapid():
        return GameFormat(timedelta(minutes=10))

    @staticmethod
    def blitz():
        return GameFormat(timedelta(minutes=5))

    @staticmethod
    def bullet():
        return GameFormat(timedelta(minutes=1))

    @staticmethod
    def from_string(value: str, time_remaining: str):
        minutes, seconds = GameFormat.__parse_time(time_remaining)

        match value:
            case "rapid":
                instance = GameFormat.rapid()
                instance._time_remaining = timedelta(minutes=minutes, seconds=seconds)
                return instance
            case "blitz":
                instance = GameFormat.blitz()
                instance._time_remaining = timedelta(minutes=minutes, seconds=seconds)
                return instance
            case "bullet":
                instance = GameFormat.bullet()
                instance._time_remaining = timedelta(minutes=minutes, seconds=seconds)
                return instance
            case _:
                raise ValueError('Invalid time input has been provided')

    def extend(self):
        pass

    @staticmethod
    def __parse_time(time_str: str):
        match = re.search(r'(?:(\d+)m)?\s*(\d+)s?', time_str)
        if match:
            minutes = int(match.group(1)) if match.group(1) else 0
            seconds = int(match.group(2))
            return minutes, seconds
        return None  # If no match found
