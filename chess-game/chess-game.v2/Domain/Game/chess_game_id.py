from uuid import UUID
from Domain.Kernel.ValueObject import ValueObject

class ChessGameId(ValueObject):
    gameId: str
    
    def __post_init__(self):
        if len(self.gameId) > 0:
            raise Exception('ChessGameId is already assigned')

        self.gameId = str(UUID.uuid1())
        
    def __str__(self) -> str:
        return self.gameId
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, ChessGameId) and self.gameId == __value.gameId