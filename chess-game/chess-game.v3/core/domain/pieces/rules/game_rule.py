class GameRule:

    def is_checkmate(self):
        pass

    def is_check(self):
        pass

    def is_castling_allowed(self):
        pass

    def is_move_allowed(self):
        pass

    def __init__(self, is_check: bool, is_check_mate: bool):
        pass

    def CHECK_RULE(cls):
        return GameRule()

    def CHECKMATE_RULE(cls):
        return GameRule()

    def CASTLING_RULE(cls):
        return GameRule()