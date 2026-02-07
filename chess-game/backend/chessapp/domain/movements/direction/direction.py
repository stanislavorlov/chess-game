from chessapp.domain.movements.direction.direction_type import DirectionType

class Direction:

    def __init__(self, type_: DirectionType):
        self._type = type_

    @staticmethod
    def forward():
        return Direction(DirectionType.Forward)

    @staticmethod
    def any():
        return Direction(DirectionType.Any)

    @staticmethod
    def diagonally():
        return Direction(DirectionType.Diagonally)

    @staticmethod
    def horizontally():
        return Direction(DirectionType.Horizontally)

    @staticmethod
    def vertically():
        return Direction(DirectionType.Vertically)

    @staticmethod
    def l_shape():
        return Direction(DirectionType.LShape)

    def __eq__(self, other):
        if isinstance(other, Direction):
            return self._type == other._type

        return False