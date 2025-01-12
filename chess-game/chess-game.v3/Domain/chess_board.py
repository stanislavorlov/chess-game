from Domain.Side import Side

class chess_board(object):
    
    def __init__(self, playerSide: Side):
        self.__initialize_board(playerSide)
        
    def __initialize_board(self, playerSide: Side):
        board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
        ]
        self._board = board
        
        if playerSide._value == Side.BLACK()._value:
            self._board.reverse()
            
    def get_board_view(self):
        return self._board
