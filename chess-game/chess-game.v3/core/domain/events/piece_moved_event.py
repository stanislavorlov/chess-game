from dataclasses import dataclass

from diator.events import DomainEvent
from core.domain.chessboard.position import Position


@dataclass(frozen=True, kw_only=True)
class PieceMovedEvent(DomainEvent):
    from_: Position
    to_: Position