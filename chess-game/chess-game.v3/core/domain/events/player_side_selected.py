from diator.requests import Request

from core.domain.value_objects.side import Side

class PlayerSideSelected(Request):
    player_side: Side