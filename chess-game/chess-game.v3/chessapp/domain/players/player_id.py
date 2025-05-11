from dataclass_factory.naming import lower
from chessapp.domain.kernel.value_object import ValueObject
from chessapp.domain.value_objects.side import Side


class PlayerId(ValueObject):

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @staticmethod
    def of(side: Side):
        return PlayerId(str(side))

    def __str__(self):
        return self._value.upper()

    def __eq__(self, other):
        if not isinstance(other, PlayerId):
            return False

        return lower(self._value) == lower(other._value)

    def __ne__(self, other):
        return not self == other