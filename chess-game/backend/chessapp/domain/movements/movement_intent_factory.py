from chessapp.domain.movements.direction.direction import Direction
from chessapp.domain.movements.movement import Movement
from chessapp.domain.movements.movement_intent import MovementIntent


class MovementIntentFactory:

    @staticmethod
    def calculate_direction(movement: Movement):
        return Direction.forward()

    @staticmethod
    def create(movement: Movement) -> MovementIntent:
        from_ = movement.from_position
        to = movement.to_position

        return MovementIntent(
            from_.file - to.file,
            from_.rank - to.rank,
            MovementIntentFactory.calculate_direction(movement))