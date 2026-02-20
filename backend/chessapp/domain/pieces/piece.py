from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.side import Side

class Piece(object):
    def __init__(self, side: Side, type_: PieceType):
        self._side = side
        self._type = type_
        self._moved = False

    @property
    def is_white(self) -> bool:
        return self._side == Side.white()

    @property
    def is_black(self) -> bool:
        return self._side == Side.black()

    @property
    def is_moved(self) -> bool:
        return self._moved

    def get_side(self):
        return self._side

    def get_abbreviation(self) -> str:
        return f"{self._side}{self._type.value}".lower()

    def get_piece_type(self):
        return self._type

    def mark_moved(self):
        self._moved = True

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self._type == other._type and self._side == other._side
        return False

    def get_points(self):
        return 0