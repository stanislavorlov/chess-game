import dataclasses
from dataclasses import dataclass
from chessapp.domain.chessboard.position import Position
from chessapp.domain.kernel.base import BaseCommand
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class MovePieceCommand(BaseCommand):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()