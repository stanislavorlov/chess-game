from datetime import datetime
from dataclasses import dataclass
from diator.events import DomainEvent
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameStarted(DomainEvent):
    game_id: ChessGameId
    started_date: datetime