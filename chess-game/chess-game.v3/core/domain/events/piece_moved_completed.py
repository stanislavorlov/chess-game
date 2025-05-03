import dataclasses
from diator.events import DomainEvent
from core.domain.chessboard.position import Position
from core.domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMovedCompleted(DomainEvent):
    game_id: ChessGameId = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()