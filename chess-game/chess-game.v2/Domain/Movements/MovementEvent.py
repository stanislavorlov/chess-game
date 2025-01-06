from Domain.Board.square import Square
from Domain.Pieces import Piece
from Domain.Movements import MoveType

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