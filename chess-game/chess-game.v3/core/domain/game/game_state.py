from typing import Optional

from core.domain.chessboard.file import File
from core.domain.chessboard.position import Position
from core.domain.chessboard.rank import Rank
from core.domain.movements.movement import Movement
from core.domain.movements.movement_intent import MovementIntent
from core.domain.pieces.piece import Piece
from core.domain.pieces.bishop import Bishop
from core.domain.pieces.king import King
from core.domain.pieces.knight import Knight
from core.domain.pieces.pawn import Pawn
from core.domain.pieces.queen import Queen
from core.domain.pieces.rook import Rook
from core.domain.value_objects.side import Side

class GameState(object):

    def __init__(self):
        self._is_check: bool = False
        self._is_check_mate: bool = False
        self._captured_pieces = []
        self._turn: Side = Side.white()

        self._state: dict[Position, Piece] = {
            Position(File.a(),Rank.r1()):Rook(Side.white()),
            Position(File.a(),Rank.r2()):Pawn(Side.white()),
            Position(File.b(),Rank.r1()):Knight(Side.white()),
            Position(File.b(),Rank.r2()):Pawn(Side.white()),
            Position(File.c(),Rank.r1()):Bishop(Side.white()),
            Position(File.c(),Rank.r2()):Pawn(Side.white()),
            Position(File.d(),Rank.r1()):Queen(Side.white()),
            Position(File.d(),Rank.r2()):Pawn(Side.white()),
            Position(File.e(),Rank.r1()):King(Side.white()),
            Position(File.e(),Rank.r2()):Pawn(Side.white()),
            Position(File.f(),Rank.r1()):Bishop(Side.white()),
            Position(File.f(),Rank.r2()):Pawn(Side.white()),
            Position(File.g(),Rank.r1()):Knight(Side.white()),
            Position(File.g(),Rank.r2()):Pawn(Side.white()),
            Position(File.h(),Rank.r1()):Rook(Side.white()),
            Position(File.h(),Rank.r2()):Pawn(Side.white()),
            Position(File.a(),Rank.r7()):Pawn(Side.black()),
            Position(File.a(),Rank.r8()):Rook(Side.black()),
            Position(File.b(),Rank.r7()):Pawn(Side.black()),
            Position(File.b(),Rank.r8()):Knight(Side.black()),
            Position(File.c(),Rank.r7()):Pawn(Side.black()),
            Position(File.c(),Rank.r8()):Bishop(Side.black()),
            Position(File.d(),Rank.r7()):Pawn(Side.black()),
            Position(File.d(),Rank.r8()):Queen(Side.black()),
            Position(File.e(),Rank.r7()):Pawn(Side.black()),
            Position(File.e(),Rank.r8()):King(Side.black()),
            Position(File.f(),Rank.r7()):Pawn(Side.black()),
            Position(File.f(),Rank.r8()):Bishop(Side.black()),
            Position(File.g(),Rank.r7()):Pawn(Side.black()),
            Position(File.g(),Rank.r8()):Knight(Side.black()),
            Position(File.h(),Rank.r7()):Pawn(Side.black()),
            Position(File.h(),Rank.r8()):Rook(Side.black())
        }

    @property
    def is_check(self) -> bool:
        return self._is_check

    @property
    def is_checkmate(self) -> bool:
        return self._is_check_mate

    @property
    def turn(self):
        return self._turn

    def init(self, player_side: Side):
        pass

    def get_state(self):
        return self._state

    def switch_turn(self):
        self._turn = Side.black() if self._turn == Side.white() else Side.white()

    def get_piece(self, position: Position) -> Piece:
        return self._state[position]

    def select_piece(self, position: Position) -> Optional[Piece]:
        return self.get_piece(position)

    def move_piece(self, movement: Movement):
        self._state.pop(movement.from_position, None)
        self._state[movement.to_position] = movement.piece

    def is_valid_move(self, movementIntent: MovementIntent):
        return False