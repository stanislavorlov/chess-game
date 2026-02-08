from datetime import datetime
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


class GameFinished(BaseEvent):
    game_id: ChessGameId
    result: str
    finished_date: datetime