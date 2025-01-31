from core.domain.events.domain_event import DomainEvent


class MovementStarted(DomainEvent):

    def __init__(self):
        super().__init__()