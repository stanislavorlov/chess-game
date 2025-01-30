import random

from domain.game_state import GameState
from domain.movements.movement_rule import MovementRule
from domain.movements.movement_specification import MovementSpecification
from domain.side import Side
from domain.chess_game import ChessGame
from interface.char_presenter import CharacterPresenter
from interface.image_presenter import ImagePresenter

sides = [Side.white(), Side.black()]
start_side = random.choice(sides)
print("Your game side:" + str(start_side))

state = GameState()
#presenter = ImagePresenter()
presenter = CharacterPresenter()
specification = MovementSpecification(MovementRule.bishop_rule(), start_side, state)

game = ChessGame(state, presenter, specification)
game.start(start_side)