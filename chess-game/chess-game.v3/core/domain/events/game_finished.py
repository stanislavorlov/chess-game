from diator.events import DomainEvent

from core.domain.value_objects.game_id import ChessGameId


class GameFinished(DomainEvent):
    game_id: ChessGameId
    result: str