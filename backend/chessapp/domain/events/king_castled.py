from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.side import Side
from ...domain.chessboard.position import Position

@dataclass(frozen=True, kw_only=True)
class KingCastled(BaseEvent):
    game_id: ChessGameId
    side: Side
    king_from: Position
    king_to: Position
    rook_from: Position
    rook_to: Position
    is_kingside: bool

    @property
    def event_type(self) -> str:
        return "king-castled"
