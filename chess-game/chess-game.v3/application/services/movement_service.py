from domain.chessboard.position import Position
from domain.movements.movement import Movement
from domain.movements.movement_intent import MovementIntent
from domain.movements.movement_specification import MovementSpecification
from domain.movements.direction.direction import Vector, Direction
from domain.pieces.piece import Piece

class MovementService:

    def calculate_direction(self):
        return Direction.forward()

    def move_piece(self, piece: Piece, from_: Position, to: Position):
        movement: Movement = Movement(piece, from_, to)
        intent = MovementIntent(from_.file - to.file, from_.rank - to.rank, self.calculate_direction())

        if self._specification.is_satisfied_by(movement):
            print('move piece')
            # update game state
            # return success action
        else:
            print('invalid move')
            # return invalid action

        # if game state allows movement

        # if chessboard allow movement
