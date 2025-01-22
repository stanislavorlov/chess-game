from domain.chessboard.position import Position
from domain.pieces.piece import Piece

class Movement:

    def __init__(self, piece: Piece, _from: Position, _to: Position):
        self._piece = piece
        self._from = _from
        self._to = _to

    @property
    def piece(self):
        return self._piece

    @property
    def from_position(self):
        return self._from

    @property
    def to_position(self):
        return self._to