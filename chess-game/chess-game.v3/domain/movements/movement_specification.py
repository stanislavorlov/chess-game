from domain.game_state import GameState
from domain.movements.movement import Movement
from domain.movements.movement_rule import MovementRule
from domain.side import Side

class MovementSpecification:

    def __init__(self, movement_rule: MovementRule, side: Side, state: GameState):
        self._movementRule = movement_rule
        self._side = side
        self._state = state

    @property
    def movement_rule(self):
        return self._movementRule

    @property
    def piece_side(self):
        return self._side

    @property
    def state(self):
        return self._state

    def is_satisfied_by(self, movement: Movement) -> bool:
        return (self._movementRule.is_allowed(movement) and
                self._state.is_valid(movement) and
                self._state.turn == self._side)