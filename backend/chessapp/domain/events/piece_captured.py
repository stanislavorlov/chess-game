import dataclasses
from ...domain.kernel.base import BaseEvent
from ...domain.pieces.piece import Piece
from ...domain.chessboard.position import Position
from ...domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceCaptured(BaseEvent):
    game_id: ChessGameId = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    # piece been captured by Piece from PieceMoved
    piece: Piece = dataclasses.field()

    @property
    def event_type(self) -> str:
        return "piece-captured"