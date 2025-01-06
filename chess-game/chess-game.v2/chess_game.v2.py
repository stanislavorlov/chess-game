from Domain.Board.chess_board import ChessBoard
from Domain.Game.chess_game import ChessGame
from Domain.Game.chess_game_id import ChessGameId
from Domain.Pieces.Side import Side
from Domain.Players.Players import Players
from Domain.painter import Painter

value = input("Choose your side WHITE or BLACK: ")
startSide = Side.BLACK if str(Side.BLACK()) == value else Side.WHITE()
print("Your game side:" + str(startSide))

chessBoard = ChessBoard()
chessGameId = ChessGameId()
players = Players()

chess_game = ChessGame()
chess_game.start(chessBoard, chessGameId, startSide, players)

painter = Painter(chess_game)
# Call the function to draw the chessboard
painter.draw()