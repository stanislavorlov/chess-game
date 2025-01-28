import abc
import uuid
from domain.pieces.piece_type import PieceType
from domain.side import Side

class Piece(object):
    def __init__(self, side: Side, type_: PieceType):
        self._id = uuid.uuid4()
        self._side = side
        self._type = type_
        
    def is_white(self) -> bool:
        return self._side == Side.white
    
    def is_black(self) -> bool:
        return self._side == Side.black

    def get_acronym(self) -> str:
        return f"{self._side}{self._type.value}".lower()

    def get_piece_id(self):
        return self._id

    def get_piece_type(self):
        return self._type

    @abc.abstractmethod
    def get_movement_rule(self):
        pass