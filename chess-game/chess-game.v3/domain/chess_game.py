from domain.side import Side
from domain.chessboard.chess_board import ChessBoard
from domain.game_state import GameState

class ChessGame(object):
    
    def __init__(self, player_side: Side):
        self._started : bool = False
        self._finished : bool = False
        self._playerSide: Side = player_side
        self._board: ChessBoard = ChessBoard()
        self._gameState: GameState = GameState(self._playerSide, self._board)
        
    def get_player_side(self) -> Side:
        return self._playerSide
            
    def select_piece(self, file, rank):
        # convert board cell into 2-d array index
        cellIdx = self._board.get_cell_idx(file, rank)
        piece = self._gameState.get_state()[cellIdx[0]][cellIdx[1]]

        if piece:
            print(f"selected piece: " + piece.get_acronym())

    def get_board(self):
        return self._board
    
    def get_state(self):
        return self._gameState.get_state()