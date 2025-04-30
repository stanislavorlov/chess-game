import uuid
from core.domain.kernel.value_object import ValueObject


class PieceId(ValueObject):

    def __init__(self, value: str):
        super().__init__()
        self._value = value

    @staticmethod
    def generate_id():
        return PieceId(str(uuid.uuid4()))

    @property
    def value(self):
        return self._value