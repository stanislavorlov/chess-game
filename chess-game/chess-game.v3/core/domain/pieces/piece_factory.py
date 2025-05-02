from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.piece_type import PieceType
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.value_objects.piece_id import PieceId
from core.domain.value_objects.side import Side


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