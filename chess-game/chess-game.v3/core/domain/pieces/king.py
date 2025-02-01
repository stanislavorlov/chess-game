from core.domain.pieces.rules.king_rule import KingRule
from core.domain.pieces.piece import Piece
from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.side import Side

class King(Piece):

    def get_rule(self):
        return KingRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.King)
        self._has_moved = False
        self._has_castled = False

    def move(self):
        self._has_moved = True

    def has_moved(self):
        return self._has_moved

    def castle(self):
        self._has_castled = True

    def has_castled(self):
        self._has_castled = True