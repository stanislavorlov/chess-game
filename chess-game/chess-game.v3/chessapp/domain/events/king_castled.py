from dataclasses import dataclass
from diator.events import DomainEvent
from chessapp.domain.value_objects.game_id import ChessGameId

@dataclass(frozen=True, kw_only=True)
class KingCastledEvent(DomainEvent):
    game_id: ChessGameId

