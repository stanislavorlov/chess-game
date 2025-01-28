from domain.chessboard.position import Position
from domain.movements.delta.delta import Delta
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

    @property
    def delta_file(self) -> Delta:
        return self._to.file - self._from.file

    @property
    def delta_rank(self) -> Delta:
        return self._to.rank - self._from.rank