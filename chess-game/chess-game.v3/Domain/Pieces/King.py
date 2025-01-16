from typing import override

from Domain.Pieces import Piece
from Domain.Pieces.PieceType import PieceType
from Domain.Side import Side

class King(Piece):

    def __init__(self, side: Side):
        super().__init__(side, PieceType.King)