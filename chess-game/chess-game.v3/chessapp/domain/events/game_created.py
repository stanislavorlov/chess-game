import dataclasses
from dataclasses import dataclass
from chessapp.domain.kernel.base import BaseEvent
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class GameCreated(BaseEvent):
    game_id: ChessGameId = dataclasses.field()