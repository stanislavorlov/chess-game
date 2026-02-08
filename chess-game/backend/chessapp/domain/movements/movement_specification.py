from ...domain.movements.movement_intent import MovementIntent
from ...domain.rules.movements.piece_rule import PieceRule


class MovementSpecification:

    def __init__(self, move_rule: PieceRule):
        self._moveRule = move_rule

    def is_satisfied_by(self, movement_intent: MovementIntent) -> bool:
        is_valid = self._moveRule.is_valid(movement_intent)

        return is_valid