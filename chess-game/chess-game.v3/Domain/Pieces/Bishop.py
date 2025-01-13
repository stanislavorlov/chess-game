from typing_extensions import override
from Domain.Pieces.Piece import Piece
from Domain.Pieces.PieceType import PieceType
from Domain.Side import Side

class Bishop(Piece):
    
    def __init__(self, side: Side):
        super().__init__(side = side, type_ = PieceType.Bishop)

    @override
    def get_acronym(self) -> str:
        return f"{self._side}B".lower()