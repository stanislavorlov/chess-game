from ...domain.pieces.bishop import Bishop
from ...domain.pieces.king import King
from ...domain.pieces.knight import Knight
from ...domain.pieces.pawn import Pawn
from ...domain.pieces.piece_type import PieceType
from ...domain.pieces.queen import Queen
from ...domain.pieces.rook import Rook
from ...domain.value_objects.side import Side


class PieceFactory(object):

    @classmethod
    def create(cls, side: Side, type_: PieceType):
        match type_:
            case PieceType.Pawn:
                return Pawn(side)
            case PieceType.King:
                return King(side)
            case PieceType.Rook:
                return Rook(side)
            case PieceType.Queen:
                return Queen(side)
            case PieceType.Bishop:
                return Bishop(side)
            case PieceType.Knight:
                return Knight(side)
        return None