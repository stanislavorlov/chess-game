import uuid

from core.domain.kernel.value_object import ValueObject


class ChessGameId(ValueObject):

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @staticmethod
    def _validate(value: str):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(f"Invalid UUID format: {value}")

    @property
    def value(self) -> str:
        return self._value

    def __eq__(self, other):
        if isinstance(other, ChessGameId):
            return self._value == other._value
        return False

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"ObjectId({self._value})"

    @staticmethod
    def generate_id():
        return ChessGameId(str(uuid.uuid4()))