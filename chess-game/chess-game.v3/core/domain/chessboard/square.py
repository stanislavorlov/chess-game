from typing import Optional
from core.domain.chessboard.position import Position
from core.domain.pieces.piece import Piece
from core.domain.value_objects.side import Side

class Square:
    def __init__(self, position: Position, piece: Optional[Piece]):
        self._position = position
        self._piece = piece

    @property
    def position(self):
        return self._position

    @property
    def color(self):
        return Side.black() if \
            ((self._position.file.to_index() +
              self._position.rank.to_index()) % 2 == 0) \
            else Side.white()

    @property
    def piece(self):
        return self._piece

    @property
    def is_occupied(self):
        return self._piece is not None