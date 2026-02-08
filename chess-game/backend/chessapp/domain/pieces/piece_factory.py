from ...domain.pieces.bishop import Bishop
from ...domain.pieces.king import King
from ...domain.pieces.knight import Knight
from ...domain.pieces.pawn import Pawn
from ...domain.pieces.piece_type import PieceType
from ...domain.pieces.queen import Queen
from ...domain.pieces.rook import Rook
from ...domain.value_objects.piece_id import PieceId
from ...domain.value_objects.side import Side


class PieceFactory(object):

    @classmethod
    def create(cls, piece_id: PieceId, side: Side, type_: PieceType):
        match type_:
            case PieceType.Pawn:
                return Pawn(piece_id, side)
            case PieceType.King:
                return King(piece_id, side)
            case PieceType.Rook:
                return Rook(piece_id, side)
            case PieceType.Queen:
                return Queen(piece_id, side)
            case PieceType.Bishop:
                return Bishop(piece_id, side)
            case PieceType.Knight:
                return Knight(piece_id, side)
        return None