import math
from datetime import timedelta
import pandas as pd
from ...domain.kernel.value_object import ValueObject


class TimeFormat(ValueObject):

    def __init__(self, main_time: timedelta, additional_time: timedelta):
        super().__init__()
        self._main = main_time
        self._additional = additional_time

    @property
    def main_time(self):
        return self._main

    @property
    def additional_time(self):
        return self._additional

    @staticmethod
    def parse_string(main: str, additional: str):
        # 5hr34m56s
        # 2h32m
        # pd.Timedelta('5hr34m56s')

        main_time = pd.Timedelta(main)
        additional_time = pd.Timedelta(additional)

        time_format = TimeFormat(main_time, additional_time)

        # if "|" in time_str:
        #     time_format._minutes, time_format._additional_minutes = tuple(map(int, time_str.split("|")))
        # else:
        #     time_format._minutes = int(time_str)

        return time_format

    def main_string(self):
        hours, remainder = divmod(self._main.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"0hr{minutes}m{seconds}s"

    def additional_string(self):
        if math.isnan(self._additional.total_seconds()):
            return "0hr0m0s"

        hours, remainder = divmod(self._additional.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"0hr{minutes}m{seconds}s"