from domain.movements.movement import Movement
from domain.movements.square import Square
from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType

class MovementSpecification:

    def is_satisfiedby(self, movement: Movement) -> bool:
        # track changes between start and destination position

        # pawn: only changes in rank by 1 or 2
        # knight: 1 rank and 2 files OR 2 ranks and 1 file
        # bishop: rank changes == file changes
        # rock: only rank changes OR only file changes

        piece: Piece = movement.piece
        _from: Square = movement.from_square
        _to: Square = movement.to_square

        match piece.get_piece_type():
            case PieceType.Pawn:
                print('Pawn validation')
            case PieceType.Queen:
                print('Queen validation')
            case PieceType.Bishop:
                return abs(_to.row - _from.row) == abs(_to.col - _from.col)

            case PieceType.King:
                print('King validation')
            case PieceType.Knight:
                print('Knight validation')
            case PieceType.Rook:
                print('Rook validation')

        return False