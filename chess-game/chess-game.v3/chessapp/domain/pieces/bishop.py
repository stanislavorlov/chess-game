from chessapp.domain.rules.movements.bishop_rule import BishopRule
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side

class Bishop(Piece):

    def get_points(self):
        return 3

    def get_rule(self):
        return BishopRule()

    def __init__(self, piece_id: PieceId, side: Side):
        super().__init__(piece_id, side, PieceType.Bishop)