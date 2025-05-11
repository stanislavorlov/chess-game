import dataclasses
from diator.events import DomainEvent
from chessapp.domain.chessboard.position import Position
from chessapp.domain.pieces.piece import Piece


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoveFailed(DomainEvent):
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    reason: str = dataclasses.field()