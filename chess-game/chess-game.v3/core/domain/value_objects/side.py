from core.domain.kernel.value_object import ValueObject


class Side(ValueObject):
    __slots__ = ['_value']
    
    @classmethod
    def white(cls):
        return cls("W")

    @classmethod
    def black(cls):
        return cls("B")
    
    def __str__(self):
        return self._value.upper()

    def value(self) -> str:
        return str(self)

    def __eq__(self, other: 'Side'):
        return str(self) == str(other)
    
    def __init__(self, value) -> None:
        super().__init__()
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string")
        
        self._value = value.lower()