from domain.movements.movement_intent import MovementIntent
from domain.movements.rules.bishop_rule import BishopRule
from domain.movements.rules.piece_rule import PieceRule
from domain.movements.rules.rook_rule import RookRule

class QueenRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        return RookRule().is_valid(movement_intent) or BishopRule().is_valid(movement_intent)