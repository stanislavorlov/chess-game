from abc import abstractmethod
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Piece(object):
    def __init__(self, side: Side, type_: PieceType):
        self._side = side
        self._type = type_
        # patternMoves
        
    def is_white(self) -> bool:
        return self._side == Side.white
    
    def is_black(self) -> bool:
        return self._side == Side.black

    def get_acronym(self) -> str:
        return f"{self._side}{self._type.value}".lower()