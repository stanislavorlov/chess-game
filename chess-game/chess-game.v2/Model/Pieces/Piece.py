from Model.Pieces.PieceType import PieceType
from Model.Pieces.Side import Side

class Piece:
    # patternMoves

    def __init__(self, side: Side, type_: PieceType):
        self._side = side
        self._type = type_
        
    def is_white(self) -> bool:
        return self._side == Side.WHITE
    
    def is_black(self) -> bool:
        return self._side == Side.BLACK