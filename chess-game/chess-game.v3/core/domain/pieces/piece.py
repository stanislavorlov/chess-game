from abc import abstractmethod

from core.domain.pieces.piece_type import PieceType
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side

class Piece(object):
    def __init__(self, piece_id: PieceId, side: Side, type_: PieceType):
        self._id = piece_id
        self._side = side
        self._type = type_
        
    def is_white(self) -> bool:
        return self._side == Side.white
    
    def is_black(self) -> bool:
        return self._side == Side.black

    def get_side(self):
        return self._side

    def get_acronym(self) -> str:
        return f"{self._side}{self._type.value}".lower()

    def get_piece_id(self):
        return self._id

    def get_piece_type(self):
        return self._type

    @abstractmethod
    def get_rule(self):
        pass