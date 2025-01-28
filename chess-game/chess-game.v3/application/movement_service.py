from domain.chessboard.position import Position
from domain.movements.movement import Movement
from domain.movements.movement_specification import MovementSpecification
from domain.movements.direction.direction import Vector
from domain.pieces.piece import Piece

class MovementService:

    def __init__(self, specification: MovementSpecification):
        self._specification = specification

    def move_piece(self, piece: Piece, from_: Position, to: Position):
        vector: Vector = Vector(from_.file - to.file, from_.rank - to.rank)
        movement: Movement = Movement(piece, from_, to)

        if self._specification.is_satisfied_by(movement):
            print('move piece')
            # update game state
            # return success action
        else:
            print('invalid move')
            # return invalid action

        # if game state allows movement

        # if chessboard allow movement
