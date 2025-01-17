from domain.side import Side

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