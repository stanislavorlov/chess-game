from Domain.Pieces import Piece
from Domain.Side import Side
from Domain.Pieces.PieceType import PieceType

class Rook(Piece):
    def __init__(self, side: Side):
        super().__init__(side, PieceType.Rook)