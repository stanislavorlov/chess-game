from Domain.Events.ChessGameDomainEvent import ChessGameDomainEvent

class Mediator:
    
    def __init__(self):
        self._handlers = {}
        
    def register_handler(self, request_type, handler):
        self._handlers[request_type] = handler
    
    def publish(self, domainEvent: ChessGameDomainEvent):
        request_type = type(domainEvent)
        if request_type in self._handlers:
            handler = self._handlers[request_type]
            
            return handler.handle(domainEvent)
        
        raise Exception(f"No handler registered for {request_type}")