import dataclasses
from ...domain.chessboard.position import Position
from ...domain.kernel.base import BaseEvent
from ...domain.pieces.piece import Piece


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoveFailed(BaseEvent):
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    reason: str = dataclasses.field()