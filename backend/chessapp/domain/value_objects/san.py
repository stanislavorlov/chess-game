from ..kernel.value_object import ValueObject

class SAN(ValueObject):
    def __init__(self, value: str):
        super().__init__()
        self._value = value

    def __str__(self):
        return self._value

    @property
    def value(self) -> str:
        return self._value
