from core.domain.movements.movement_intent import MovementIntent
from core.domain.pieces.rules.bishop_rule import BishopRule
from core.domain.pieces.rules.piece_rule import PieceRule
from core.domain.pieces.rules.rook_rule import RookRule

class QueenRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        return RookRule().is_valid(movement_intent) or BishopRule().is_valid(movement_intent)