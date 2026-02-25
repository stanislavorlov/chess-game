from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent
from ...domain.value_objects.game_id import ChessGameId
from ...domain.value_objects.side import Side
from ...domain.chessboard.position import Position
from ...domain.pieces.piece_type import PieceType


@dataclass(frozen=True, kw_only=True)
class PawnPromoted(BaseEvent):
    game_id: ChessGameId
    side: Side
    to: Position
    promoted_to: PieceType
    time_taken: float = 0.0

    @property
    def event_type(self) -> str:
        return "pawn-promoted"