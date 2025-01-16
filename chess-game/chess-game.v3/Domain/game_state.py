from Domain.Side import Side
from Domain.Pieces.Bishop import Bishop
from Domain.Pieces.King import King
from Domain.Pieces.Knight import Knight
from Domain.Pieces.Pawn import Pawn
from Domain.Pieces.Queen import Queen
from Domain.Pieces.Rook import Rook

class game_state(object):
    
    def __init__(self, playerSide: Side):
        self._playerSide = playerSide
        self._state = []
        self.__initialize_game(self._playerSide)

    def __initialize_game(self, playerSide: Side):
        state = [
            [ Rook(Side.BLACK()), Knight(Side.BLACK()), Bishop(Side.BLACK()), Queen(Side.BLACK()), King(Side.BLACK()), Bishop(Side.BLACK()), Knight(Side.BLACK()), Rook(Side.BLACK()) ],
            [ Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()), Pawn(Side.BLACK()) ],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ None, None, None, None, None, None, None, None],
            [ Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE()), Pawn(Side.WHITE())],
            [ Rook(Side.WHITE()), Knight(Side.WHITE()), Bishop(Side.WHITE()), Queen(Side.WHITE()), King(Side.WHITE()), Bishop(Side.WHITE()), Knight(Side.WHITE()), Rook(Side.WHITE())],
        ]
        
        if playerSide._value == Side.BLACK()._value:
            state.reverse()

        self._state = state
        
    def get_state(self):
        return self._state