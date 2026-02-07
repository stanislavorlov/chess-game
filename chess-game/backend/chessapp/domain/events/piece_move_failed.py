import dataclasses
from chessapp.domain.chessboard.position import Position
from chessapp.domain.kernel.base import BaseEvent
from chessapp.domain.pieces.piece import Piece


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoveFailed(BaseEvent):
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    reason: str = dataclasses.field()