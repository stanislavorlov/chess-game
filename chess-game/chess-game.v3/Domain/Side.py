class Side:
    __slots__ = ['_value']
    
    @classmethod
    def WHITE(cls):
        return cls("W")

    @classmethod
    def BLACK(cls):
        return cls("B")
    
    def __str__(self):
        return self._value.upper()
    
    def __init__(self, value) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string")
        
        self._value = value.lower()