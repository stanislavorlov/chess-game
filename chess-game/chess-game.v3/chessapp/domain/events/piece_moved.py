import dataclasses
from diator.events import DomainEvent
from chessapp.domain.chessboard.position import Position
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclasses.dataclass(frozen=True, kw_only=True)
class PieceMoved(DomainEvent):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()