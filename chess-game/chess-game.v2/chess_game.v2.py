from Model.Game.chess_game import ChessGame
from Model.painter import Painter

chess_game = ChessGame()

painter = Painter(chess_game)
# Call the function to draw the chessboard
painter.draw()