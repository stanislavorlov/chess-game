from Domain.Pieces.Bishop import Bishop
from Domain.Side import Side
from Domain.chess_game import chess_game
from Interface.presenter import presenter

bishop = Bishop(Side.BLACK())
print(bishop.get_acronym())

value = input("Choose your side WHITE or BLACK: ")
startSide = Side.BLACK() if str(Side.BLACK()) == value else Side.WHITE()
print("Your game side:" + str(startSide))

game = chess_game(startSide)

p = presenter(game)
p.draw()