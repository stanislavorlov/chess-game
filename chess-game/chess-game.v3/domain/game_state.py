from typing import Optional

from domain.chessboard.position import Position
from domain.movements.movement import Movement
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
        self._state: dict[Position, Piece] = {
            Position("a",1):Rook(Side.white()),
            Position("a",2):Pawn(Side.white()),
            Position("b",1):Knight(Side.white()),
            Position("b",2):Pawn(Side.white()),
            Position("c",1):Bishop(Side.white()),
            Position("c",2):Pawn(Side.white()),
            Position("d",1):Queen(Side.white()),
            Position("d",2):Pawn(Side.white()),
            Position("e",1):King(Side.white()),
            Position("e",2):Pawn(Side.white()),
            Position("f",1):Bishop(Side.white()),
            Position("f",2):Pawn(Side.white()),
            Position("g",1):Knight(Side.white()),
            Position("g",2):Pawn(Side.white()),
            Position("h",1):Rook(Side.white()),
            Position("h",2):Pawn(Side.white()),
            Position("a",7):Pawn(Side.black()),
            Position("a",8):Rook(Side.black()),
            Position("b",7):Pawn(Side.black()),
            Position("b",8):Knight(Side.black()),
            Position("c",7):Pawn(Side.black()),
            Position("c",8):Bishop(Side.black()),
            Position("d",7):Pawn(Side.black()),
            Position("d",8):Queen(Side.black()),
            Position("e",7):Pawn(Side.black()),
            Position("e",8):King(Side.black()),
            Position("f",7):Pawn(Side.black()),
            Position("f",8):Bishop(Side.black()),
            Position("g",7):Pawn(Side.black()),
            Position("g",8):Knight(Side.black()),
            Position("h",7):Pawn(Side.black()),
            Position("h",8):Rook(Side.black())
        }

    def init(self, player_side: Side):
        pass

    def get_state(self):
        return self._state

    def get_piece(self, position: Position) -> Piece:
        return self._state[position]

    def select_piece(self, position: Position) -> Optional[Piece]:
        return self.get_piece(position)

    def move_piece(self, movement: Movement):
        self._state.pop(movement.from_position, None)
        self._state[movement.to_position] = movement.piece