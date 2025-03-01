from core.domain.rules.movements.bishop_rule import BishopRule
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side

class Bishop(Piece):

    def get_points(self):
        return 3

    def get_rule(self):
        return BishopRule()

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.Bishop)