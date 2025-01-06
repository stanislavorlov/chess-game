from Domain.Events.DomainEventId import DomainEventId

class ChessGameDomainEvent(object):
    
    def __init__(self, eventId: DomainEventId):
        self._eventId = eventId