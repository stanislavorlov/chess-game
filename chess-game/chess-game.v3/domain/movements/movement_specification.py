from domain.chessboard.chess_board import ChessBoard
from domain.chessboard.position import Position
from domain.movements.movement import Movement
from domain.pieces.piece import Piece
from domain.pieces.piece_type import PieceType

class MovementSpecification:

    def __init__(self, board: ChessBoard):
        self._board = board

    def is_satisfied(self, movement: Movement) -> bool:
        # track changes between start and destination position

        # pawn: only changes in rank by 1 or 2
        # knight: 1 rank and 2 files OR 2 ranks and 1 file
        # bishop: rank changes == file changes
        # rock: only rank changes OR only file changes

        piece: Piece = movement.piece
        _from: Position = movement.from_position
        _to: Position = movement.to_position

        match piece.get_piece_type():
            case PieceType.Pawn:
                print('Pawn validation')
            case PieceType.Queen:
                print('Queen validation')
            case PieceType.Bishop:
                from_idx = self._board.index_of(_from)
                to_idx = self._board.index_of(_to)

                return abs(to_idx[0] - from_idx[0]) == abs(to_idx[1] - from_idx[1])

            case PieceType.King:
                print('King validation')
            case PieceType.Knight:
                print('Knight validation')
            case PieceType.Rook:
                print('Rook validation')

        return False