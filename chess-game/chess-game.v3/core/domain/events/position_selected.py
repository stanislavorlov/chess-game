from domain.events.domain_event import DomainEvent


class PositionSelected(DomainEvent):

    def __init__(self):
        super().__init__()
