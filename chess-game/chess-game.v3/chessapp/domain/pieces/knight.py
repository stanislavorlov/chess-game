from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.rules.movements.knight_rule import KnightRule
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side


class Knight(Piece):

    def get_points(self):
        return 3

    def get_rule(self):
        return KnightRule()

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.Knight)