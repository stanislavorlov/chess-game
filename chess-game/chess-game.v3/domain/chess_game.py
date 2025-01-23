from typing import Optional

from domain.chessboard.position import Position
from domain.movements.movement import Movement
from domain.movements.movement_specification import MovementSpecification
from domain.pieces.piece import Piece
from domain.side import Side
from domain.game_state import GameState
from interface.presenter import Presenter

class ChessGame(object):

    def __init__(self, state: GameState, presenter: Presenter, specification: MovementSpecification):
        self._started : bool = False
        self._finished : bool = False
        self._selectedPiece: Optional[Piece] = None
        self._fromPosition: Optional[Position] = None
        self._toPosition: Optional[Position] = None
        self._gameState: GameState = state
        self._presenter: Presenter = presenter
        self._moveSpecification: MovementSpecification = specification

        self._presenter.bind_canvas_click_function(onclick_callback=self.click_square)

    def start(self, player_side: Side):
        self._started = True
        self._gameState.init(player_side)
        self._presenter.draw(self._gameState)

    def click_square(self, position: Position):
        if not self._selectedPiece:
            self._selectedPiece = self._gameState.select_piece(position)
            self._fromPosition = position
        else:
            self._toPosition = position
            movement: Movement = Movement(self._selectedPiece, self._fromPosition, self._toPosition)
            if self._moveSpecification.is_satisfied(movement):
                self._gameState.move_piece(movement)
                self._selectedPiece = None
                self._presenter.draw(self._gameState)
            else:
                print('invalid movement')