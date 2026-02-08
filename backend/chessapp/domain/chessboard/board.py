from typing import List
from ...domain.chessboard.file import File
from ...domain.chessboard.position import Position
from ...domain.chessboard.rank import Rank
from ...domain.chessboard.square import Square
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.pawn_promoted import PawnPromoted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_moved import PieceMoved
from ...domain.kernel.value_object import ValueObject
from ...domain.movements.movement import Movement
from ...domain.pieces.bishop import Bishop
from ...domain.pieces.king import King
from ...domain.pieces.knight import Knight
from ...domain.pieces.pawn import Pawn
from ...domain.pieces.queen import Queen
from ...domain.pieces.rook import Rook
from ...domain.value_objects.piece_id import PieceId
from ...domain.value_objects.side import Side


class Board(ValueObject):

    def __init__(self):
        super().__init__()
        self._board: dict[Position, Square] = {}
        self.__board_initialize__(self._board)

    def piece_moved(self, piece_moved: PieceMoved):
        piece = piece_moved.piece
        from_ = piece_moved.from_
        to = piece_moved.to

        self._board[from_] = Square(from_, None)
        self._board[to] = Square(to, piece)

    def piece_captured(self, piece_captured: PieceCaptured):
        pass

    def pawn_promoted(self, pawn_promoted: PawnPromoted):
        pass

    def king_checked(self, king_checked: KingChecked):
        pass

    def king_checkmated(self, king_checkmated: KingCheckMated):
        pass

    def search_available_moves(self) -> List[Movement]:
        list_of_moves = []

        # ToDo: bitboard
        # https://github.com/cglouch/snakefish/blob/master/src/tables.py
        # https://www.frayn.net/beowulf/theory.html#bitboards

        # ToDo: stockfish
        # https://official-stockfish.github.io/docs/stockfish-wiki/Developers.html

        for position, square in self._board.items():
            move = Movement(square.piece, position, position)

            list_of_moves.append(move)

        return list_of_moves

    @staticmethod
    def __board_initialize__(board: dict[Position, Square]):
        for file in File.a():
            for rank in Rank.r1():
                piece_color = Side.white() if rank in (Rank.r1(), Rank.r2()) else Side.black()
                position = Position(file, rank)

                if rank in (Rank.r2(), Rank.r7()):
                    board[position] = Square(position, Pawn(PieceId.generate_id(), piece_color))
                elif rank in (Rank.r1(), Rank.r8()):
                    if file in (File.a(), File.h()):
                        board[position] = Square(position, Rook(PieceId.generate_id(), piece_color))
                    elif file in (File.b(), File.g()):
                        board[position] = Square(position, Knight(PieceId.generate_id(), piece_color))
                    elif file in (File.c(), File.f()):
                        board[position] = Square(position, Bishop(PieceId.generate_id(), piece_color))
                    elif file == File.d():
                        board[position] = Square(position, Queen(PieceId.generate_id(), piece_color))
                    else:
                        board[position] = Square(position, King(PieceId.generate_id(), piece_color))
                else:
                    board[position] = Square(position, None)

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item: Position):
        return self._board[item]