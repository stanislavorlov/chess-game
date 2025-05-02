import dataclasses

from diator.requests import Request
from core.domain.chessboard.position import Position
from core.domain.pieces.piece import Piece
from core.domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoved(Request):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()