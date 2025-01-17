from enum import Enum

class PieceType(str, Enum):
    King = "K"
    Queen = "Q"
    Bishop = "B"
    Knight = "N"
    Rook = "R"
    Pawn = "P"