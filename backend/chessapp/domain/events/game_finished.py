from dataclasses import dataclass
from datetime import datetime
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameFinished(BaseEvent):
    game_id: ChessGameId
    result: str
    finished_date: datetime

    @property
    def event_type(self) -> str:
        return "game-finished"