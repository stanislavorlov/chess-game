from Model.Game.chess_game import ChessGame
from Model.painter import Painter

gameSide = input("Choose your side WHITE or BLACK: ")
print("Your game side:" + gameSide)

chess_game = ChessGame()

painter = Painter(chess_game)
# Call the function to draw the chessboard
painter.draw()