import dataclasses

from diator.events import DomainEvent
from core.domain.chessboard.position import Position
from core.domain.pieces.piece import Piece


class PieceMoved(DomainEvent):
    piece: Piece = dataclasses.field()
    from_: Position = dataclasses.field()
    to: Position = dataclasses.field()