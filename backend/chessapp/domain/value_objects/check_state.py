from typing import Optional
from chessapp.domain.chessboard.position import Position
from chessapp.domain.kernel.value_object import ValueObject
from chessapp.domain.value_objects.side import Side


class CheckState(ValueObject):

    def __init__(self, check_side: Optional[Side], check_position: Optional[Position]):
        super().__init__()
        self._check_side = check_side
        self._check_position = check_position

    @property
    def side_checked(self) -> Side:
        return self._check_side

    @property
    def position_checked(self) -> Position:
        return self._check_position

    @staticmethod
    def default():
        return CheckState(check_side=None, check_position=None)

    @staticmethod
    def white_checked(king_position: Position):
        return CheckState(check_side=Side.white(), check_position=king_position)

    @staticmethod
    def black_checked(king_position: Position):
        return CheckState(check_side=Side.black(), check_position=king_position)