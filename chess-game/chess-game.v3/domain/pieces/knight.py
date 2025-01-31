from domain.movements.rules.knight_rule import KnightRule
from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Knight(Piece):

    def get_rule(self):
        return KnightRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Knight)