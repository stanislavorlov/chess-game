from datetime import timedelta
from ...domain.kernel.value_object import ValueObject
from ...domain.value_objects.time_format import TimeFormat


class GameFormat(ValueObject):

    def __init__(self, time_remaining: TimeFormat, value: str):
        super().__init__()
        self._time_remaining = time_remaining
        self._value = value

        self.__validate_format(value, time_remaining.base_time, time_remaining.move_increment)

    @staticmethod
    def rapid(time_remaining: TimeFormat):
        return GameFormat(time_remaining, "rapid")

    @staticmethod
    def blitz(time_remaining: TimeFormat):
        return GameFormat(time_remaining, "blitz")

    @staticmethod
    def bullet(time_remaining: TimeFormat):
        return GameFormat(time_remaining, "bullet")

    @staticmethod
    def parse_string(
        value: str,
        time_remaining: str,
        move_increment: str
    ):
        match value:
            case "rapid":
                instance = GameFormat.rapid(TimeFormat.parse_string(time_remaining, move_increment))
                return instance
            case "blitz":
                instance = GameFormat.blitz(TimeFormat.parse_string(time_remaining, move_increment))
                return instance
            case "bullet":
                instance = GameFormat.bullet(TimeFormat.parse_string(time_remaining, move_increment))
                return instance
            case _:
                raise ValueError('Invalid time input has been provided')

    def to_string(self):
        return self._value

    @property
    def time_remaining(self) -> TimeFormat:
        return self._time_remaining

    def extend(self):
        pass

    @staticmethod
    def __validate_format(format_: str, base_time: timedelta, increment: timedelta) -> bool:
        base_minutes = divmod(base_time.total_seconds(), 60)[0]
        inc_seconds = increment.total_seconds()
        
        allowed_options = {
            "bullet": [(1, 0), (1, 1), (2, 1)],
            "blitz": [(3, 0), (3, 2), (5, 0)],
            "rapid": [(10, 0), (15, 10), (30, 0)]
        }

        if format_ not in allowed_options:
            raise ValueError(f"Invalid format: {format_}")

        if (base_minutes, inc_seconds) not in allowed_options[format_]:
            raise ValueError(f"Unsupported time control for {format_}: {base_minutes}m | {inc_seconds}s")

        return True
