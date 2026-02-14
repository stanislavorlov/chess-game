from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.side import Side

class Queen(Piece):

    def get_points(self):
        return 90

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Queen)