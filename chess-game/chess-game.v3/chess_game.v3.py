import random

from domain.chessboard.chess_board import ChessBoard
from domain.game_state import GameState
from domain.movements.movement_specification import MovementSpecification
from domain.side import Side
from domain.chess_game import ChessGame
from interface.presenter import Presenter

sides = [Side.white(), Side.black()]
start_side = random.choice(sides)
print("Your game side:" + str(start_side))

board = ChessBoard()
state = GameState()
presenter = Presenter(board)
specification = MovementSpecification(board)

game = ChessGame(board, state, presenter, specification)
game.start(start_side)