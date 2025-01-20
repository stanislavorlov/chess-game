from typing import Optional

from domain.pieces.piece import Piece
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

    def start(self, player_side: Side):
        self._started = True
        self._gameState.init(player_side)

    def get_player_side(self) -> Side:
        return self._playerSide

    def click_square(self, file: str, rank: int):
        position: (int,int) = self._board.get_position(file, rank)


    def get_board(self):
        return self._board

    def get_state(self):
        return self._gameState.get_state()