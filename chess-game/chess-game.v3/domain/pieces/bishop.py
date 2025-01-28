from domain.movements.movement_rule import MovementRule
from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Bishop(Piece):

    def __init__(self, side: Side):
        super().__init__(side, PieceType.Bishop)

    def get_movement_rule(self):
        return MovementRule.bishop_rule()