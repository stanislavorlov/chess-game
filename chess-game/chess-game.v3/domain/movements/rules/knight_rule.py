from domain.movements.delta.delta import Delta
from domain.movements.movement_intent import MovementIntent
from domain.movements.rules.piece_rule import PieceRule

class KnightRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()

        return (delta_file, delta_rank) in [(Delta.one(), Delta(2)), (Delta(2), Delta.one())]