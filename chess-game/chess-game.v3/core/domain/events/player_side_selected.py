from core.domain.events.domain_event import DomainEvent
from core.domain.value_objects.side import Side

class PlayerSideSelected(DomainEvent):

    def __init__(self, player_side: Side):
        super().__init__()
        self._player_side = player_side