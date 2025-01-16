from enum import Enum

class PieceType(str, Enum):
    King = "K"
    Queen = "Q"
    Bishop = "B"
    Knight = "K"
    Rook = "R"
    Pawn = "P"