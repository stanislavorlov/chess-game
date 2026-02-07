from chessapp.domain.rules.game_rule import GameRule


class CastlingRule(GameRule):

    def __init__(self):
        super().__init__()