import dataclasses
from dataclasses import dataclass
from ...domain.chessboard.position import Position
from ...domain.kernel.base import BaseCommand
from ...domain.pieces.piece import Piece
from ...domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class MovePieceCommand(BaseCommand):
    game_id: ChessGameId = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()
    piece: Piece = dataclasses.field()
    captured: Piece = dataclasses.field()