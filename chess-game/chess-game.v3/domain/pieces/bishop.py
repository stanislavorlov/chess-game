from domain.movements.rules.bishop_rule import BishopRule
from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Bishop(Piece):

    def get_rule(self):
        return BishopRule()

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Bishop)