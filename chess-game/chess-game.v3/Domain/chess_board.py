from Domain.Side import Side

class chess_board(object):
    
    def __init__(self, playerSide: Side):
        self._board = self.__get_player_board(playerSide)
        # Chessboard labels
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._ranks = list(range(8, 0, -1))
        
    def __get_player_board(self, playerSide: Side):
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
        
        if playerSide._value == Side.BLACK()._value:
            board.reverse()

        return board
            
    def get_board_view(self):
        return self._board

    def get_files(self):
        return self._files
    
    def get_ranks(self):
        return self._ranks