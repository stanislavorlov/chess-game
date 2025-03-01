from core.domain.game.game_format import GameFormat


class GameSettings:

    def __init__(self, format_: GameFormat):
        self._format = format_