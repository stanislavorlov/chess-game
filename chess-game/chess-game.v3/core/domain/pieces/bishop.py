from core.domain.pieces.rules.bishop_rule import BishopRule
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.side import Side

class Bishop(Piece):

    def get_rule(self):
        return BishopRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Bishop)