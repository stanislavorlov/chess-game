from dataclasses import dataclass
from diator.events import DomainEvent

from core.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameCreated(DomainEvent):
    game_id: ChessGameId