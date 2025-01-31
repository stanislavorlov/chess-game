from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.pieces.rules.knight_rule import KnightRule
from core.domain.value_objects.side import Side


class Knight(Piece):

    def get_rule(self):
        return KnightRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Knight)