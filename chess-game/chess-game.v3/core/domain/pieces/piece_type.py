from enum import Enum


class PieceType(str, Enum):
    King = "K"
    Queen = "Q"
    Bishop = "B"
    Knight = "N"
    Rook = "R"
    Pawn = "P"

    @classmethod
    def value_of(cls, value: str):
        match value:
            case "K":
                return cls.King
            case "Q":
                return cls.Queen
            case "B":
                return cls.Bishop
            case "N":
                return cls.Knight
            case "R":
                return cls.Rook
            case "P":
                return cls.Pawn
            case _:
                raise Exception(f"Unknown type: {value}")