from Domain.Side import Side

class game_state(object):
    
    def __init__(self, playerSide: Side):
        self._playerSide = playerSide
        self._state = []
        self.__initialize_game(self._playerSide)

    def __initialize_game(self, playerSide: Side):
        state = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"]
        ]

        # ToDo: array of pieces instead of strings
        
        if playerSide._value == Side.BLACK()._value:
            state.reverse()

        self._state = state
        
    def get_state(self):
        return self._state