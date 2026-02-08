from ...domain.pieces.piece import Piece
from ...domain.pieces.piece_type import PieceType
from ...domain.rules.movements.rook_rule import RookRule
from ...domain.value_objects.piece_id import PieceId
from ...domain.value_objects.side import Side


class Rook(Piece):

    def get_points(self):
        return 5

    def get_rule(self):
        return RookRule()

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.Rook)