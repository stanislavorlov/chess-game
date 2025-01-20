from typing import Optional

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
        self._selectedRow: int = -1
        self._selectedCol: int = -1

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

    def get_piece(self, row, col) -> Piece:
        return self._state[row][col]

    def select_piece(self, row, col) -> bool:
        self._selectedPiece:Optional[Piece] = self._state[row][col]
        self._selectedRow = row
        self._selectedCol = col

        if self._selectedPiece:
            print(f"selected piece: {self._selectedPiece.get_acronym()}")

            return  True

        return False

    def move_selected_piece(self, row, col):
        # ToDo: validation
        self._state[self._selectedRow][self._selectedCol] = None
        self._state[row][col] = self._selectedPiece
        self._selectedRow = -1
        self._selectedCol = -1
        self._selectedPiece = None

        return True
