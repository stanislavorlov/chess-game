from datetime import datetime
from dataclasses import dataclass
from chessapp.domain.kernel.base import BaseEvent
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameStarted(BaseEvent):
    game_id: ChessGameId
    started_date: datetime