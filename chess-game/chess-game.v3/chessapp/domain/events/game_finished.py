from datetime import datetime
from diator.events import DomainEvent
from chessapp.domain.value_objects.game_id import ChessGameId


class GameFinished(DomainEvent):
    game_id: ChessGameId
    result: str
    finished_date: datetime