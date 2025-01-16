from Domain.Pieces.Piece import Piece
from Domain.Side import Side
from Domain.Pieces.PieceType import PieceType

class Queen(Piece):
    def __init__(self, side: Side):
        super().__init__(side, PieceType.Queen)