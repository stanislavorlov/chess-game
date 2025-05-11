from chessapp.domain.movements.delta.delta import Delta
from chessapp.domain.movements.direction.direction import Direction
from chessapp.domain.movements.movement_intent import MovementIntent
from chessapp.domain.rules.movements.piece_rule import PieceRule


class PawnRule(PieceRule):

    def __init__(self, moved: bool):
        self._has_moved = moved

    def is_valid(self, movement_intent: MovementIntent) -> bool:
        delta_file, delta_rank = movement_intent.get_deltas()

        if self._has_moved:
            return movement_intent.get_direction() == Direction.forward() and \
                delta_rank == Delta.one() and not delta_file.has_changed()
        else:
            return movement_intent.get_direction() == Direction.forward() and \
                (delta_rank == Delta.one() or delta_rank == Delta(2)) and not delta_file.has_changed()