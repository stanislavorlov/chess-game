from Domain.Side import Side

class chess_board(object):
    
    def __init__(self):
        # Chessboard labels
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._ranks = list(range(8, 0, -1))

    def get_files(self):
        return self._files
    
    def get_ranks(self):
        return self._ranks