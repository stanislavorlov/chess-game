from domain.side import Side
from domain.chess_game import ChessGame
from interface.presenter import Presenter

value = input("Choose your side W (white) or B (black): ")
startSide = Side.black() if str(Side.black()) == value else Side.white()
print("Your game side:" + str(startSide))

game = ChessGame(startSide)

p = Presenter(game)
p.draw()