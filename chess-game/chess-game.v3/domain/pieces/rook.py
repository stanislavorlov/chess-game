from domain.pieces.piece import Piece
from domain.side import Side
from domain.pieces.piece_type import PieceType

class Rook(Piece):
    def __init__(self, side: Side):
        super().__init__(side, PieceType.Rook)