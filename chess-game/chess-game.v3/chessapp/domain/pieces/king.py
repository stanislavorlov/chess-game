import math
from chessapp.domain.rules.movements.king_rule import KingRule
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side

class King(Piece):

    def get_points(self):
        return math.inf

    def get_rule(self):
        return KingRule()

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.King)
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