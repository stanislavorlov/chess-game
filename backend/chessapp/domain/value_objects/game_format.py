from datetime import timedelta
from ...domain.kernel.value_object import ValueObject
from ...domain.value_objects.time_format import TimeFormat


class GameFormat(ValueObject):

    def __init__(self, time_remaining: TimeFormat, value: str):
        super().__init__()
        self._time_remaining = time_remaining
        self._value = value

        self.__validate_format(value, time_remaining.main_time)
        #self.__validate_format(value, time_remaining.additional_time)

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
    def parse_string(value: str, time_remaining: str, additional: str):
        match value:
            case "rapid":
                instance = GameFormat.rapid(TimeFormat.parse_string(time_remaining, additional))
                return instance
            case "blitz":
                instance = GameFormat.blitz(TimeFormat.parse_string(time_remaining, additional))
                return instance
            case "bullet":
                instance = GameFormat.bullet(TimeFormat.parse_string(time_remaining, additional))
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

    # @staticmethod
    # def __parse_time(time_str: str):
    #     match = re.search(r'(?:(\d+)m)?\s*(\d+)s?', time_str)
    #     if match:
    #         minutes = int(match.group(1)) if match.group(1) else 0
    #         seconds = int(match.group(2))
    #         return minutes, seconds
    #     return None  # If no match found

    @staticmethod
    def __validate_format(format_: str, time: timedelta) -> bool:
        time_minutes = divmod(time.total_seconds(), 60)[0]
        match format_:
            case "rapid":
                if time_minutes < 10 or time_minutes > 30:
                    raise ValueError('Un-supported format')
            case "blitz":
                if not 2 <= divmod(time.total_seconds(), 60)[0] <= 5:
                    raise ValueError('Un-supported format')
            case "bullet":
                if not 1 <= divmod(time.total_seconds(), 60)[0] < 3:
                    raise ValueError('Un-supported format')

        return True
