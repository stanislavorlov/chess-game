from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.side import Side

class Knight(Piece):

    def get_points(self):
        return 30

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Knight)