from dataclasses import dataclass

from diator.events import DomainEvent
from core.domain.chessboard.position import Position


@dataclass(frozen=True, kw_only=True)
class PieceNotMovedEvent(DomainEvent):
    from_: Position
    to_: Position
    reason: str