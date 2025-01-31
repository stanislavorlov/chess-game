from domain.movements.rules.queen_rule import QueenRule
from domain.pieces.piece import Piece
from domain.side import Side
from domain.pieces.piece_type import PieceType

class Queen(Piece):

    def get_rule(self):
        return QueenRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Queen)