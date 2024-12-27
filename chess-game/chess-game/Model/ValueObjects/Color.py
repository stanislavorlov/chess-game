from Model.Kernel.ValueObject import ValueObject

class Color(ValueObject):
    __slots__ = ['_value']
    
    @classmethod
    def WHITE(cls):
        return cls("white")

    @classmethod
    def BLACK(cls):
        return cls("black")
    
    def __post_init__(self):
        if not isinstance(self._value, str):
            raise ValueError(f"Value must be a string")
        
        if self._value:
            raise ValueError(f"Value is already set")
        
        object.__setattr__(self, "value", self._value.lower())