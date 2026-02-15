from dataclasses import dataclass
from ..chessboard.position import Position
from ..value_objects.side import Side
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class KingChecked(BaseEvent):
    game_id: ChessGameId
    side: Side          # which King is checked
    position: Position  # exact position of King

    @property
    def event_type(self) -> str:
        return "king-checked"