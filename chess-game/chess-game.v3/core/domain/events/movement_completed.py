from core.domain.events.domain_event import DomainEvent


class MovementCompleted(DomainEvent):
    
    def __init__(self):
        super().__init__()