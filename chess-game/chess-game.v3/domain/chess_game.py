from typing import Optional

from domain.movements.movement import Movement
from domain.movements.movement_specification import MovementSpecification
from domain.movements.square import Square
from domain.pieces.piece import Piece
from domain.side import Side
from domain.chessboard.chess_board import ChessBoard
from domain.game_state import GameState
from interface.presenter import Presenter


class ChessGame(object):

    def __init__(self, board: ChessBoard, state: GameState, presenter: Presenter, specification: MovementSpecification):
        self._started : bool = False
        self._finished : bool = False
        self._selectedPiece: Optional[Piece] = None
        self._fromSquare: Optional[Square] = None
        self._toSquare: Optional[Square] = None
        self._board: ChessBoard = board
        self._gameState: GameState = state
        self._presenter: Presenter = presenter
        self._moveSpecification: MovementSpecification = specification

        self._presenter.bind_canvas_click_function(onclick_callback=self.click_square)

    def start(self, player_side: Side):
        self._started = True
        self._gameState.init(player_side)
        self._presenter.draw(self._gameState)

    def click_square(self, file: str, rank: int):
        square: Square = self._board.get_square(file, rank)

        if not self._selectedPiece:
            self._selectedPiece = self._gameState.select_piece(square)
            self._fromSquare = square
        else:
            self._toSquare = square
            movement: Movement = Movement(self._selectedPiece, self._fromSquare, self._toSquare)
            if self._moveSpecification.is_satisfiedby(movement):
                self._gameState.move_piece(square)
                self._selectedPiece = None
                self._presenter.draw(self._gameState)
            else:
                print('invalid movement')