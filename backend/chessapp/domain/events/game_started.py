from datetime import datetime
from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameStarted(BaseEvent):
    game_id: ChessGameId
    started_date: datetime