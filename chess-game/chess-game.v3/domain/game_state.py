from domain.side import Side
from domain.pieces.bishop import Bishop
from domain.pieces.king import King
from domain.pieces.knight import Knight
from domain.pieces.pawn import Pawn
from domain.pieces.queen import Queen
from domain.pieces.rook import Rook

class GameState(object):
    
    def __init__(self, playerSide: Side):
        self._playerSide = playerSide
        self._state = []
        self.__initialize_game(self._playerSide)

    def __initialize_game(self, playerSide: Side):
        state = [
            [Rook(Side.black()), Knight(Side.black()), Bishop(Side.black()), Queen(Side.black()), King(Side.black()), Bishop(Side.black()), Knight(Side.black()), Rook(Side.black())],
            [Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black()), Pawn(Side.black())],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white()), Pawn(Side.white())],
            [Rook(Side.white()), Knight(Side.white()), Bishop(Side.white()), Queen(Side.white()), King(Side.white()), Bishop(Side.white()), Knight(Side.white()), Rook(Side.white())],
        ]
        
        if playerSide._value == Side.black()._value:
            state.reverse()

        self._state = state
        
    def get_state(self):
        return self._state