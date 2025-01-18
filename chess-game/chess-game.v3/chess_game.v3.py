import random

from domain.side import Side
from domain.chess_game import ChessGame
from interface.presenter import Presenter

sides = [Side.white(), Side.black()]
start_side = random.choice(sides)
print("Your game side:" + str(start_side))

game = ChessGame(start_side)

p = Presenter(game)
p.draw()