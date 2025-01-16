from Domain.Pieces.Piece import Piece
from Domain.Pieces.PieceType import PieceType
from Domain.Side import Side

class Bishop(Piece):

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Bishop)