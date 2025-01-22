from domain.chessboard.position import Position

class ChessBoard(object):
    
    def __init__(self):
        # Chessboard labels
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._ranks = list(range(8, 0, -1))
        self._board = {}

        for rankIdx, rank in enumerate(self._ranks):
            for fileIdx, file in enumerate(self._files):
                self._board[Position(file, rank)] = (fileIdx, rankIdx)

    def index_of(self, position: Position) -> tuple[int,int]:
        return self._board[position]

    def get_files(self):
        return self._files
    
    def get_ranks(self):
        return self._ranks

    def is_valid_square(self, file: str, rank: int) -> bool:
        return self._board.get(Position(file, rank), -1) != -1