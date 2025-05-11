from chessapp.domain.pieces.bishop import Bishop
from chessapp.domain.pieces.king import King
from chessapp.domain.pieces.knight import Knight
from chessapp.domain.pieces.pawn import Pawn
from chessapp.domain.pieces.piece_type import PieceType
from chessapp.domain.pieces.queen import Queen
from chessapp.domain.pieces.rook import Rook
from chessapp.domain.value_objects.piece_id import PieceId
from chessapp.domain.value_objects.side import Side


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