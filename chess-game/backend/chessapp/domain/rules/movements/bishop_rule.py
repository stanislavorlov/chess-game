from chessapp.domain.movements.movement_intent import MovementIntent
from chessapp.domain.rules.movements.piece_rule import PieceRule

class BishopRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()

        return delta_file == delta_rank