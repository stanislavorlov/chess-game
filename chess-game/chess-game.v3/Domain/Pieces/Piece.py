from abc import abstractmethod
from Domain.Pieces.PieceType import PieceType
from Domain.Side import Side

class Piece(object):
    def __init__(self, side: Side, type_: PieceType):
        self._side = side
        self._type = type_
        # patternMoves
        
    def is_white(self) -> bool:
        return self._side == Side.WHITE
    
    def is_black(self) -> bool:
        return self._side == Side.BLACK
    
    @abstractmethod
    def get_acronym(self) -> str:
        pass