from ..kernel.value_object import ValueObject

class UCI(ValueObject):
    def __init__(self, value: str):
        super().__init__()
        self._value = value

    def __str__(self):
        return self._value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def from_positions(cls, from_pos, to_pos):
        return cls(f"{str(from_pos)}{str(to_pos)}")
