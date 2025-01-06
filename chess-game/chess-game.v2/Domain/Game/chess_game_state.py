from Domain.Board.chess_board import ChessBoard
from Domain.Game.chess_game_id import ChessGameId
from Domain.Players.Players import Players

class ChessGameState(object):
    def __init__(self):
        self._id : ChessGameId = None
        self._board : ChessBoard = None
        self._players : Players = None
        self._started : bool = False
        self._finished : bool = False
        