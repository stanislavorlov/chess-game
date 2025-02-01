from threading import Timer
from typing import Optional

from core.domain.chessboard.position import Position
from core.domain.game.game_format import GameFormat
from core.domain.game.game_state import GameState
from core.domain.movements.movement import Movement
from core.domain.movements.movement_specification import MovementSpecification
from core.domain.pieces.piece import Piece
from core.domain.value_objects.game_id import ChessGameId
from core.domain.value_objects.side import Side
from core.interface.abstract_presenter import AbstractPresenter


class ChessGame(object):

    def __init__(self, game_id: ChessGameId, player_side: Side, state: GameState, game_format: GameFormat):
        self._game_id = game_id
        self._state = state
        self._started: bool = False
        self._finished: bool = False
        self._game_format = game_format
        self._player_side = player_side
        #self._timer = Timer(60.0 * 10, self.stop)

    def __init__2(self, state: GameState, presenter: AbstractPresenter, specification: MovementSpecification):
        # ToDo: generic unique ID of the game

        self._started : bool = False
        self._finished : bool = False
        self._selectedPiece: Optional[Piece] = None
        self._fromPosition: Optional[Position] = None
        self._toPosition: Optional[Position] = None
        self._gameState: GameState = state
        self._presenter: AbstractPresenter = presenter
        self._moveSpecification: MovementSpecification = specification
        self._timer = Timer(60.0 * 10, self.stop)

        self._presenter.onclick_handler(callback=self.make_action)

    def start(self, player_side: Side):
        self._started = True
        self._gameState.init(player_side)
        self._presenter.draw(self._gameState)
        self._timer.start()

    def make_action(self, position: Position):
        selected_piece = self._gameState.select_piece(position)

        if (not self._selectedPiece) or (selected_piece and selected_piece.get_side() == self._selectedPiece.get_side()):
            self.select_piece(selected_piece, position)
        else:
            self._toPosition = position
            movement: Movement = Movement(self._selectedPiece, self._fromPosition, self._toPosition)
            if self._moveSpecification.is_satisfied_by(movement):
                self._gameState.move_piece(movement)
                self._selectedPiece = None
                self._presenter.draw(self._gameState)
            else:
                print('invalid movement')

        # ToDo: return action instead: MOVE, SELECT, TAKE, CASTLING, CHECK, CHECKMATE, PROMOTE

    def select_piece(self, piece: Piece, position: Position):
        self._selectedPiece = piece
        self._fromPosition = position

    def stop(self):
        print('end game')