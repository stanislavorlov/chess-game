from domain.movements.square import Square
from domain.pieces.piece import Piece

class Movement:

    def __init__(self, piece: Piece, _from: Square, _to: Square):
        self._piece = piece
        self._from = _from
        self._to = _to

    @property
    def piece(self):
        return self._piece

    @property
    def from_square(self):
        return self._from

    @property
    def to_square(self):
        return self._to