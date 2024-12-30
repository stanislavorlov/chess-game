from enum import Enum

class Side:
    __slots__ = ['_value']
    
    @classmethod
    def WHITE(cls):
        return cls("W")

    @classmethod
    def BLACK(cls):
        return cls("B")
    
    def __str__(self):
        return self._value.upper()
    
    def __init__(self, value) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Value must be a string")
        
        self._value = value.lower()

class PieceType(Enum):
    King = 1
    Queen = 2
    Bishop = 3
    Knight = 4
    Rook = 5
    Pawn = 6

class Piece:
    # patternMoves

    def __init__(self, side: Side, type_: PieceType):
        self._side = side
        self._type = type_
        
    def is_white(self) -> bool:
        return self._side == Side.WHITE
    
    def is_black(self) -> bool:
        return self._side == Side.BLACK
    
class Pawn(Piece):
    pass
class Rook(Piece):
    pass
class Knight(Piece):
    pass
class Bishop(Piece):
    pass
class Queen(Piece):
    pass
class King(Piece):
    pass

class Square:
    def __init__(self, file: str, rank: str):
        self.file = file.lower() # Column ('a' to 'h')
        self.rank = rank.lower() # Row ('1' to '8')

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank

    def __str__(self):
        return f"{self.file}{self.rank}"
    
class MoveType(Enum):
    NORMAL = 1
    ATTACK = 2

class MovementEvent:
    def __init__(self, from_: Square, to: Square, piece: Piece, type_: MoveType):
        self._from: Square = from_
        self._to: Square = to
        self._piece: Piece = piece
        self._type: MoveType = type_
        
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, MovementEvent) and \
            self._piece == __value.piece and self._type == __value._type and \
            self._type == __value._type
        
class MovementSpecification:
    def __init__(self) -> None:
        pass
    
    def is_satisfied_by() -> bool:
        return True
    
class ChessGameHistory:
    def __init__(self, history: []):
        self._gameHistory = history
        
    @staticmethod
    def get_empty() -> []:
        return []
    
    def record(self, entry: MovementEvent):
        self._gameHistory.append(entry)
        
    def last(self) -> MovementEvent:
        return self._gameHistory[-1]