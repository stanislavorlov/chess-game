from typing import Optional

from domain.movements.square import Square
from domain.pieces.bishop import Bishop
from domain.pieces.king import King
from domain.pieces.knight import Knight
from domain.pieces.pawn import Pawn
from domain.pieces.piece import Piece
from domain.pieces.queen import Queen
from domain.pieces.rook import Rook
from domain.side import Side

class GameState(object):
    
    def __init__(self):
        self._state = []
        self._selectedPiece: Optional[Piece] = None
        self._selectedSquare: Optional[Square] = None

    def init(self, player_side: Side):
        state = [
            [
                Rook(Side.black()),
                Knight(Side.black()),
                Bishop(Side.black()),
                Queen(Side.black()),
                King(Side.black()),
                Bishop(Side.black()),
                Knight(Side.black()),
                Rook(Side.black())
            ],
            [
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black()),
                Pawn(Side.black())
            ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white()),
                Pawn(Side.white())
            ],
            [
                Rook(Side.white()),
                Knight(Side.white()),
                Bishop(Side.white()),
                Queen(Side.white()),
                King(Side.white()),
                Bishop(Side.white()),
                Knight(Side.white()),
                Rook(Side.white())
            ],
        ]

        if str(player_side) == str(Side.black()):
            state.reverse()

        self._state = state

    def get_state(self):
        return self._state

    def get_piece(self, square: Square) -> Piece:
        return self._state[square.row][square.col]

    def select_piece(self, square: Square) -> Optional[Piece]:
        self._selectedPiece:Optional[Piece] = self.get_piece(square)
        self._selectedSquare = square

        return self._selectedPiece

    def move_piece(self, square: Square):
        if self._selectedSquare:
            self._state[self._selectedSquare.row][self._selectedSquare.col] = None
        self._state[square.row][square.col] = self._selectedPiece
        self._selectedSquare = None
        self._selectedPiece = None

        return True

    def get_selected_piece(self) -> Optional[Piece]:
        return  self._selectedPiece