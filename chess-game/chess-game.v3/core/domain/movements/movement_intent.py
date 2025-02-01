from core.domain.movements.delta.delta import Delta
from core.domain.movements.direction.direction import Direction

class MovementIntent:

    def __init__(self, delta_file: Delta, delta_rank: Delta, direction: Direction):
        self._delta_file = delta_file
        self._delta_rank = delta_rank
        self._direction = direction

    def get_deltas(self):
        return self._delta_file, self._delta_rank

    def get_direction(self):
        return self._direction