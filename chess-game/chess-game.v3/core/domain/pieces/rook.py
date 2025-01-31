from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.pieces.rules.rook_rule import RookRule
from core.domain.value_objects.side import Side


class Rook(Piece):

    def get_rule(self):
        return RookRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Rook)