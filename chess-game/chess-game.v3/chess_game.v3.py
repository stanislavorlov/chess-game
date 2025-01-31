import random

from application.handlers.movement_completed_handler import MovementCompletedHandler
from application.handlers.movement_started_handler import MovementStartedHandler
from application.handlers.piece_selected_handler import PieceSelectedHandler
from domain.events.movement_completed import MovementCompleted
from domain.events.movement_started import MovementStarted
from domain.events.piece_selected import PieceSelected
from domain.game_state import GameState
from domain.side import Side
from domain.chess_game import ChessGame
from infrastructure.mediator import Mediator
from interface.char_presenter import CharacterPresenter
from interface.image_presenter import ImagePresenter

sides = [Side.white(), Side.black()]
start_side = random.choice(sides)
print("Your game side:" + str(start_side))

state = GameState()
#presenter = ImagePresenter()
presenter = CharacterPresenter()

mediator = Mediator()
mediator.bind(MovementCompleted, MovementCompletedHandler)
mediator.bind(MovementStarted, MovementStartedHandler)
mediator.bind(PieceSelected, PieceSelectedHandler)

game = ChessGame(state, presenter, specification)
game.start(start_side)