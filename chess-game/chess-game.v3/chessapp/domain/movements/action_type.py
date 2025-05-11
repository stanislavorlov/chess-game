from enum import Enum

class ActionType(Enum):
    SELECT = 1
    MOVE = 2
    TAKE = 3
    CASTLING = 4
    CHECK = 5
    CHECKMATE = 6
    PROMOTE = 7
    PASSANT = 8