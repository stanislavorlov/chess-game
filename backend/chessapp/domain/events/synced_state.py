import dataclasses
from typing import List
from dataclasses import dataclass
from ..value_objects.side import Side
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class SyncedState(BaseEvent):
    game_id: ChessGameId
    turn: Side
    legal_moves: List[dict] = dataclasses.field(default_factory=list)

    @property
    def event_type(self) -> str:
        return "synced-state"
