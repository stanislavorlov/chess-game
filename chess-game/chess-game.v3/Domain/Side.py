class Side:
    __slots__ = ['_value']
    
    @classmethod
    def WHITE(cls):
        return cls("WHITE")

    @classmethod
    def BLACK(cls):
        return cls("BLACK")
    
    def __str__(self):
        return self._value.upper()
    
    def __init__(self, value) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string")
        
        self._value = value.lower()
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Side):
            return self._value == other._value
        
        return False