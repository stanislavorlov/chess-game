from domain.events.domain_event import DomainEvent


class PieceSelected(DomainEvent):
    
    def __init__(self):
        super().__init__()