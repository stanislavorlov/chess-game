from core.domain.movements.direction.direction import Direction
from core.domain.movements.movement_intent import MovementIntent
from core.domain.rules.movements.piece_rule import PieceRule


class PawnRule(PieceRule):

    def __init__(self, moved: bool):
        self._has_moved = moved

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()
        if self._has_moved:
            return movement_intent.get_direction() == Direction.forward() and \
                delta_rank == 1 and not delta_file.has_changed()
        else:
            return movement_intent.get_direction() == Direction.forward() and \
                (delta_rank == 1 or delta_rank == 2) and not delta_file.has_changed()