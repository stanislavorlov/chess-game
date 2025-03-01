from core.domain.kernel.value_object import ValueObject


class GameStatus(ValueObject):
    __slots__ = ['_value']

    @classmethod
    def started(cls):
        return cls("STARTED")

    @classmethod
    def finished(cls):
        return cls("FINISHED")

    def __init__(self, value: str):
        super().__init__()

        self._value = value
