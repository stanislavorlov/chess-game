import uuid
from Domain.Kernel.ValueObject import ValueObject

class ChessGameId(ValueObject):
    __slots__ = ['_gameId']
    
    def __init__(self):
        self._gameId = str(uuid.uuid4())
        
    def __str__(self) -> str:
        return self._gameId
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ChessGameId) and self._gameId == __value._gameId
    
    def __hash__(self) -> int:
        return hash(self._gameId)