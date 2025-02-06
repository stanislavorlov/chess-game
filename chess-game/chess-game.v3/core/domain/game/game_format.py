from core.domain.kernel.value_object import ValueObject


class GameFormat(ValueObject):

    def __init__(self, time_minutes: int):
        super().__init__()
        self._time_minutes = time_minutes

    @staticmethod
    def rapid():
        return GameFormat(10)

    @staticmethod
    def blitz():
        return GameFormat(5)

    @staticmethod
    def bullet():
        return GameFormat(1)

    def extend(self):
        pass
