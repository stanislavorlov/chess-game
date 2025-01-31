import random

from core.application.handlers.movement_completed_handler import MovementCompletedHandler
from core.application.handlers.movement_started_handler import MovementStartedHandler
from core.application.handlers.piece_selected_handler import PieceSelectedHandler
from core.domain.events.movement_completed import MovementCompleted
from core.domain.events.movement_started import MovementStarted
from core.domain.events.piece_selected import PieceSelected
from core.domain.game.game_state import GameState
from core.domain.value_objects.side import Side
from core.domain.game.chess_game import ChessGame
from core.infrastructure.mediator import Mediator
from core.interface.char_presenter import CharacterPresenter

# ToDo: move all this logic into ChessGame object
# ToDo: Store ChessGame into repo
# ToDo: no direct invocation between objects, only Events and handlers

sides = [Side.white(), Side.black()]
start_side = random.choice(sides)
print("Your game side:" + str(start_side))

# Once selected publish PlayerSideSelected event

state = GameState()
#presenter = ImagePresenter()
presenter = CharacterPresenter()

mediator = Mediator()
mediator.bind(MovementCompleted, MovementCompletedHandler)
mediator.bind(MovementStarted, MovementStartedHandler)
mediator.bind(PieceSelected, PieceSelectedHandler)

game = ChessGame(state, presenter, specification)
game.start(start_side)