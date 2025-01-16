from domain.side import Side
from domain.chess_board import ChessBoard
from domain.game_state import GameState

class ChessGame(object):
    
    def __init__(self, playerSide: Side):
        self._started : bool = False
        self._finished : bool = False
        self._playerSide: Side = playerSide
        self._gameState: GameState = GameState(self._playerSide)
        self._board: ChessBoard = ChessBoard()
        
    def get_playerSide(self) -> Side:
        return self._playerSide
            
    def select_piece(self, file, rank):
        print(f"selected piece: ")

    def get_board(self):
        return self._board
    
    def get_state(self):
        return self._gameState.get_state()