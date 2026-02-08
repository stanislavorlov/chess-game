import dataclasses
from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameCreated(BaseEvent):
    game_id: ChessGameId = dataclasses.field()