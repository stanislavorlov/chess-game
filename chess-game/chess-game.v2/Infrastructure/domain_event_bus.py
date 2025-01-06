from Domain.Events.ChessGameDomainEvent import ChessGameDomainEvent

class DomainEventBus:
    
    def __init__(self) -> None:
        pass
    
    def publish(self, domainEvent: ChessGameDomainEvent):
        pass