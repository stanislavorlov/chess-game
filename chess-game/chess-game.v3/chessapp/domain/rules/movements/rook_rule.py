from chessapp.domain.movements.movement_intent import MovementIntent
from chessapp.domain.rules.movements.piece_rule import PieceRule


class RookRule(PieceRule):

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()

        return (delta_file.has_changed() and not delta_rank.has_changed()) or \
            (delta_rank.has_changed() and not delta_file.has_changed())