import dataclasses
from dataclasses import dataclass
from diator.requests import Request
from chessapp.domain.chessboard.position import Position
from chessapp.domain.pieces.piece import Piece
from chessapp.domain.value_objects.game_id import ChessGameId


@dataclass(frozen=True, kw_only=True)
class MovePieceCommand(Request):
    game_id: ChessGameId = dataclasses.field()
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()