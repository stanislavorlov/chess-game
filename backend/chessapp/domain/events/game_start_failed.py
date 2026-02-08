from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameStartFailed(BaseEvent):
    game_id: ChessGameId

    @property
    def event_type(self) -> str:
        return "game-start-failed"