from domain.chessboard.position import Position
from domain.movements.square import Square


class ChessBoard(object):
    
    def __init__(self):
        # Chessboard labels
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._ranks = list(range(8, 0, -1))
        self._board = {}

        for rankIdx, rank in enumerate(self._ranks):
            for fileIdx, file in enumerate(self._files):
                self._board[Position(file, rank)] = (fileIdx, rankIdx)

    def get_files(self):
        return self._files
    
    def get_ranks(self):
        return self._ranks

    def get_square(self, file: str, rank: int) -> Square:
        (col, row) = self._board[Position(file, rank)]

        return  Square(row, col)