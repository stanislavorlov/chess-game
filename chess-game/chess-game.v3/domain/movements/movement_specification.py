from domain.game_state import GameState
from domain.movements.movement_intent import MovementIntent
from domain.movements.rules.piece_rule import PieceRule
from domain.side import Side

class MovementSpecification:

    def __init__(self, side: Side, move_rule: PieceRule, state: GameState):
        self._side = side
        self._state = state
        self._moveRule = move_rule

    @property
    def piece_side(self):
        return self._side

    @property
    def state(self):
        return self._state

    def is_satisfied_by(self, movement_intent: MovementIntent) -> bool:
        return self._moveRule.is_valid(movement_intent) and \
                self._state.is_valid_move(movement_intent) and \
                self._state.turn == self._side