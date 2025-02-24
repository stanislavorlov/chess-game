import dataclasses

from diator.events import DomainEvent

from core.domain.chessboard.position import Position
from core.domain.pieces.piece import Piece


@dataclasses.dataclass(frozen=True, kw_only=True)
class PiecePositioned(DomainEvent):
    piece: Piece = dataclasses.field()
    position: Position = dataclasses.field()