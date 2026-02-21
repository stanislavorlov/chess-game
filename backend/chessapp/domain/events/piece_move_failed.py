import dataclasses
from ..chessboard.position import Position
from ..kernel.base import BaseEvent
from ..pieces.piece import Piece
from ..value_objects.game_id import ChessGameId
from ...domain.value_objects.move_failure_reason import MoveFailureReason


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoveFailed(BaseEvent):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    reason: MoveFailureReason = dataclasses.field()

    @property
    def event_type(self) -> str:
        return "piece-move-failed"