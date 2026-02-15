from ...domain.kernel.value_object import ValueObject


class GameStatus(ValueObject):
    __slots__ = ['_value']

    @classmethod
    def created(cls):
        return cls("CREATED")

    @classmethod
    def started(cls):
        return cls("STARTED")

    @classmethod
    def finished(cls):
        return cls("FINISHED")

    @classmethod
    def aborted(cls):
        return cls("ABORTED")

    def __str__(self):
        return self._value

    def __eq__(self, other: 'GameStatus'):
        if isinstance(other, GameStatus):
            return self._value == other._value

        return False

    def __init__(self, value: str):
        super().__init__()

        self._value = value
