from domain.movements.rules.rook_rule import RookRule
from domain.pieces.piece import Piece
from domain.side import Side
from domain.pieces.piece_type import PieceType

class Rook(Piece):

    def get_rule(self):
        return RookRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Rook)