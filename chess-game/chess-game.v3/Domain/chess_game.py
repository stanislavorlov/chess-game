from Domain.Side import Side

class chess_game(object):
    
    def __init__(self, playerSide: Side):
        self._started : bool = False
        self._finished : bool = False
        self._playerSide: Side = playerSide
        
        self.__initialize_board()
        
    def get_playerSide(self) -> Side:
        return self._playerSide
    
    def get_board(self):
        return self._board
    
    def __initialize_board(self):
        
        if self._playerSide == Side.WHITE():

            self._board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
            
        else:
            
            self._board = [
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ]