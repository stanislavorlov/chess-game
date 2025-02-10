from core.domain.players.player_id import PlayerId


class Players:

    def __init__(self, white_player: PlayerId, black_player: PlayerId):
        self._white = white_player
        self._black = black_player