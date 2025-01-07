from Domain.Board.chess_board import ChessBoard
from Domain.Events.ChessGameStartedEvent import ChessGameStartedEvent
from Domain.Game.chess_game import ChessGame
from Domain.Game.chess_game_id import ChessGameId
from Domain.Pieces.Side import Side
from Domain.Players.Players import Players
from Domain.painter import Painter
from Infrastructure.Handlers.chess_game_started_handler import ChessGameStartedHandler
from Infrastructure.mediator import Mediator

value = input("Choose your side WHITE or BLACK: ")
startSide = Side.BLACK if str(Side.BLACK()) == value else Side.WHITE()
print("Your game side:" + str(startSide))

mediator = Mediator()
mediator.register_handler(ChessGameStartedEvent, ChessGameStartedHandler)

chessBoard = ChessBoard()
chessGameId = ChessGameId()
players = Players()

chess_game = ChessGame(mediator)
chess_game.start(chessBoard, chessGameId, startSide, players)

painter = Painter(chess_game)
# Call the function to draw the chessboard
painter.draw()

input("Press enter to exit;")