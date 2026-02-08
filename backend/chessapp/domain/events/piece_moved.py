import dataclasses
from ...domain.chessboard.position import Position
from ...domain.kernel.base import BaseEvent
from ...domain.pieces.piece import Piece
from ...domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoved(BaseEvent):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()

    @property
    def event_type(self) -> str:
        return "piece-moved"