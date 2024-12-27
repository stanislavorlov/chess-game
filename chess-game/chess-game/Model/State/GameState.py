from collections import defaultdict
from Model.Board.Board import Board
from Model.Kernel.AggregateRoot import AggregateRoot
from Model.Pieces.Bishop import Bishop
from Model.Pieces.King import King
from Model.Pieces.Knight import Knight
from Model.Pieces.Pawn import Pawn
from Model.Pieces.Queen import Queen
from Model.Pieces.Rook import Rook
from Model.ValueObjects.Color import Color

class GameState(AggregateRoot):
    
    def __init__(self):
        super().__init__()
        self._board = Board()
        self._state = defaultdict()
        self._current_turn = Color.WHITE
        self.move_history = []                  # List of moves made in the game
        self.captured_pieces = []               # List of captured pieces
        self.is_check = False                   # Whether the current player is in check
        self.is_checkmate = False               # Whether the game is in checkmate
        self.is_stalemate = False               # Whether the game is in stalemate
        
        self.__init_pieces__()
        
    def place_pieces(self, piece_class, positions, color):
        for position in positions:
            self._board.place_piece(piece_class(id=f"{color[0]}_{piece_class.__name__.lower()}_{position}", color=color), position)

    def __init_pieces__(self):
        # white player
        # 8 Pawns, 2 Rooks (♖), 2 Knights (♘), 2 Bishops (♗), Queen, King

        # back player
        # 8 Pawns, 2 Rooks (♖), 2 Knights (♘), 2 Bishops (♗), Queen, King

        # K - King, Q - Queen, B - Bishop, N - Knight, R - Rook, P - Pawn

        # Pawns
        for file in "abcdefgh":
            self._board.place_piece(Pawn(id=f"wp_{file}", color=Color.WHITE), f"{file}2")
            self._board.place_piece(Pawn(id=f"bp_{file}", color=Color.BLACK), f"{file}7")
            
            self._state[f"{file}2"] = Pawn(id=f"wp_{file}", color=Color.WHITE, position= f"{file}2")
            self._state[f"{file}7"] = Pawn(id=f"bp_{file}", color=Color.BLACK, position= f"{file}7")

        # Rooks
        self.place_pieces(Rook, ["a1", "h1"], Color.WHITE)
        self.place_pieces(Rook, ["a8", "h8"], Color.BLACK)
        
        

        # Knights
        self.place_pieces(Knight, ["b1", "g1"], Color.WHITE)
        self.place_pieces(Knight, ["b8", "g8"], Color.BLACK)

        # Bishops
        self.place_pieces(Bishop, ["c1", "f1"], Color.WHITE)
        self.place_pieces(Bishop, ["c8", "f8"], Color.BLACK)

        # Queens
        self.place_pieces(Queen, ["d1"], Color.WHITE)
        self.place_pieces(Queen, ["d8"], Color.BLACK)

        # Kings
        self.place_pieces(King, ["e1"], Color.WHITE)
        self.place_pieces(King, ["e8"], Color.BLACK)