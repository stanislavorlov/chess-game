from domain.movements.direction.direction import Direction
from domain.movements.movement_intent import MovementIntent
from domain.movements.rules.piece_rule import PieceRule
from domain.pieces.pawn import Pawn

class PawnRule(PieceRule):

    def __init__(self, piece: Pawn):
        self._piece = piece

    def is_valid(self, movement_intent: MovementIntent):
        delta_file, delta_rank = movement_intent.get_deltas()
        if self._piece.has_moved():
            return movement_intent.get_direction() == Direction.forward() and \
                delta_rank == 1 and not delta_file.has_changed()
        else:
            return movement_intent.get_direction() == Direction.forward() and \
                (delta_rank == 1 or delta_rank == 2) and not delta_file.has_changed()