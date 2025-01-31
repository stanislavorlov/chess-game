from domain.movements.movement_intent import MovementIntent
from domain.movements.rules.piece_rule import PieceRule
from domain.pieces.king import King

class KingRule(PieceRule):

    def __init__(self, piece: King):
        self._piece = piece

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()

        return max(delta_file, delta_rank) == 1