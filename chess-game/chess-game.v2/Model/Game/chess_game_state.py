from Model.Board.chess_board import ChessBoard
from Model.Game.chess_game_id import ChessGameId
from Model.Players.Players import Players

class ChessGameState(object):
    def __init__(self):
        self._id : ChessGameId = None
        self._board : ChessBoard = None
        self._players : Players = None
        
        