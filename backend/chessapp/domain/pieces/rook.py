from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.side import Side

class Rook(Piece):

    def get_points(self):
        return 50

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Rook)
        self._has_moved = False

    def move(self):
        self._has_moved = True

    def has_moved(self):
        return self._has_moved