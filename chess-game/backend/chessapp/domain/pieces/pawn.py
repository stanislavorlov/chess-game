from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.rules.movements.pawn_rule import PawnRule
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side


class Pawn(Piece):

    def get_points(self):
        return 1

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.Pawn)
        self._has_moved = False

    def move(self):
        self._has_moved = True

    def has_moved(self):
        return self._has_moved

    def get_rule(self):
        return PawnRule(self._has_moved)

    def promote(self):
        pass