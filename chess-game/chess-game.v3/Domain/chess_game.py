from Domain.Side import Side
from Domain.chess_board import chess_board
from Domain.game_state import game_state

class chess_game(object):
    
    def __init__(self, playerSide: Side):
        self._started : bool = False
        self._finished : bool = False
        self._playerSide: Side = playerSide
        self._gameState: game_state = game_state()
        self._board: chess_board = chess_board(self._playerSide)
        
        # self.__initialize_board()
        
    def get_playerSide(self) -> Side:
        return self._playerSide
    
    # def get_board(self):
    #     return self._board
    
    # def __initialize_board(self):
    #     board = [
    #         ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    #         ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    #         [None, None, None, None, None, None, None, None],
    #         [None, None, None, None, None, None, None, None],
    #         [None, None, None, None, None, None, None, None],
    #         [None, None, None, None, None, None, None, None],
    #         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    #         ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
    #     ]
    #     self._board = board
        
    #     if self._playerSide._value == Side.BLACK()._value:
    #         self._board.reverse()
            
    def select_piece(self, file, rank):
        print(f"selected piece: ")