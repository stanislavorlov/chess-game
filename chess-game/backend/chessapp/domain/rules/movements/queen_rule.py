from chessapp.domain.movements.movement_intent import MovementIntent
from chessapp.domain.rules.movements.bishop_rule import BishopRule
from chessapp.domain.rules.movements.piece_rule import PieceRule
from chessapp.domain.rules.movements.rook_rule import RookRule

class QueenRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        return RookRule().is_valid(movement_intent) or BishopRule().is_valid(movement_intent)