from domain.movements.delta.delta import Delta
from domain.movements.delta.operator import Operator
from domain.movements.direction.direction import Direction
from domain.movements.movement import Movement
from domain.pieces.piece_type import PieceType

class MovementRule:

    @staticmethod
    def pawn_rule():
        # Moves one square forward, but on its first move, it can move two squares forward.
        return MovementRule(Direction.forward(), Delta.zero(), Delta.one(), Operator.and_())

        #return MovementRule(Operator.or_(Operator.and_(Direction.forward(), Delta.zero(), Delta.one())),
        #                    Operator.and_(Direction.forward(), Delta.zero(), Delta(2)))

    @staticmethod
    def king_rule():
        # moves 1 square in any direction
        return MovementRule(Direction.any(), Delta.one(), Delta.one(), Operator.or_())

    @staticmethod
    def bishop_rule():
        # Moves any number of squares diagonally.
        return MovementRule(Direction.any(), Delta.any(), Delta.any(), Operator.equal())

    @staticmethod
    def rook_rule():
        # moves any number of squares horizontally or vertically.
        return MovementRule()

    @staticmethod
    def knight_rule():
        # Moves in an ‘L-shape,’ two squares in a straight direction, and then one square perpendicular to that.
        return MovementRule()

    @staticmethod
    def queen_rule():
        # moves any numbers of squares diagonally, horizontally, or vertically.
        return MovementRule.bishop_rule() or MovementRule.rook_rule()

    def __init__(self, direction: Direction, delta_file: Delta, delta_rank: Delta, delta_operator: Operator):
        self._direction = direction
        self._delta_file = delta_file
        self._delta_rank = delta_rank
        self._operator = delta_operator

    def is_allowed(self, movement: Movement) -> bool:
        return False