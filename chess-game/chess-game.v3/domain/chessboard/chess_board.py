from domain.chessboard.position import Position


class ChessBoard(object):
    
    def __init__(self):
        # Chessboard labels
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._ranks = list(range(8, 0, -1))

    def get_files(self):
        return self._files
    
    def get_ranks(self):
        return self._ranks

    def get_cell_idx(self, file, rank):
        return [self._ranks.index(rank), self._files.index(file)]

    def get_position_by_file_rank_idx(self, file: int, rank: int):
        return Position(self._files[file], str(rank))