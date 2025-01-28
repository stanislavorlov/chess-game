from enum import Enum

class DirectionType(int, Enum):
    Any = 0
    Forward = 1
    Diagonally = 2
    Horizontally = 3
    Vertically = 4
    LShape = 5