from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.pieces.rules.queen_rule import QueenRule
from core.domain.value_objects.side import Side


class Queen(Piece):

    def get_rule(self):
        return QueenRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Queen)