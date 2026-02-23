from ...domain.kernel.value_object import ValueObject


class GameStatus(ValueObject):
    __slots__ = ['_value', '_rank']

    @classmethod
    def created(cls):
        return cls("CREATED", 0)

    @classmethod
    def started(cls):
        return cls("STARTED", 1)

    @classmethod
    def finished(cls):
        return cls("FINISHED", 2)

    @classmethod
    def aborted(cls):
        return cls("ABORTED", 3)

    def __str__(self):
        return self._value

    def __eq__(self, other: 'GameStatus'):
        if isinstance(other, GameStatus):
            return self._value == other._value

        return False

    def __init__(self, value: str, rank: int):
        super().__init__()

        self._value = value
        self._rank = rank

    def is_following_rank(self, other: 'GameStatus'):
        return self._rank >= other._rank