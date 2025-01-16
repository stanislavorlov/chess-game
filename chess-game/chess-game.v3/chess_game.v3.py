from Domain.Side import Side
from Domain.chess_game import chess_game
from Interface.presenter import Presenter

value = input("Choose your side W (white) or B (black): ")
startSide = Side.BLACK() if str(Side.BLACK()) == value else Side.WHITE()
print("Your game side:" + str(startSide))

game = chess_game(startSide)

p = Presenter(game)
p.draw()