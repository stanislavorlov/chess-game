from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Knight(Piece):

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Knight)