from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.pieces.rules.pawn_rule import PawnRule
from core.domain.value_objects.side import Side


class Pawn(Piece):

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Pawn)
        self._has_moved = False

    def move(self):
        self._has_moved = True

    def has_moved(self):
        return self._has_moved

    def get_rule(self):
        return PawnRule(self._has_moved)

    def promote(self):
        pass