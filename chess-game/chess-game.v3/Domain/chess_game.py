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
        board = []
        
        if self._playerSide == Side.WHITE():
            board.append(["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"])
            board.append(["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"])
        else:
            board.append(["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"])
            board.append(["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"])
            
        board.append([None, None, None, None, None, None, None, None])
        board.append([None, None, None, None, None, None, None, None])
        board.append([None, None, None, None, None, None, None, None])
        board.append([None, None, None, None, None, None, None, None])
        
        if self._playerSide == Side.WHITE():
            board.append(["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"])
            board.append(["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"])
        else:
            board.append(["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"])
            board.append(["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"])

        self._board = board