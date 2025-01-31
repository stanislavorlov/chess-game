from domain.value_objects.side import Side


class PlayerSideSelected:

    def __init__(self, player_side: Side):
        self._player_side = player_side