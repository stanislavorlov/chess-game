from Domain.Side import Side
from Domain.chess_board import chess_board
from Domain.game_state import game_state

class chess_game(object):
    
    def __init__(self, playerSide: Side):
        self._started : bool = False
        self._finished : bool = False
        self._playerSide: Side = playerSide
        self._gameState: game_state = game_state(self._playerSide)
        self._board: chess_board = chess_board()
        
    def get_playerSide(self) -> Side:
        return self._playerSide
            
    def select_piece(self, file, rank):
        print(f"selected piece: ")

    def get_board(self):
        return self._board
    
    def get_state(self):
        return self._gameState.get_state()