from typing import Optional

from domain.chessboard.position import Position
from domain.pieces.piece import Piece
from domain.side import Side
from domain.chessboard.chess_board import ChessBoard
from domain.game_state import GameState
from interface.presenter import Presenter


class ChessGame(object):

    def __init__(self, board: ChessBoard, state: GameState, presenter: Presenter):
        self._started : bool = False
        self._finished : bool = False
        self._isPieceSelected: bool = False

        self._board: ChessBoard = board
        self._gameState: GameState = state
        self._presenter: Presenter = presenter

        self._presenter.bind_canvas_click_function(onclick_callback=self.click_square)

    def start(self, player_side: Side):
        self._started = True
        self._gameState.init(player_side)
        self._presenter.draw(self._gameState)

    def click_square(self, file: str, rank: int):
        print(f"ChessGame click handler {file}{rank}")
        position: (int,int) = self._board.get_position(file, rank)

        # if piece is not selected than select it
        if not self._isPieceSelected:
            self._isPieceSelected = self._gameState.select_piece(position[1], position[0])
        # otherwise move to selected square
        else:
            self._gameState.move_piece(position[1], position[0])
            self._isPieceSelected = False
            self._presenter.update_piece()

        self._presenter.draw(self._gameState)