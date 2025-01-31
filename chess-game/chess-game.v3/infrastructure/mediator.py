from application.handlers.base_handler import BaseHandler
from domain.events.domain_event import DomainEvent


class Mediator:

    def __init__(self):
        self._handlers = {}

    def bind(self, request_type, handler):
        self._handlers[request_type] = handler

    def publish(self, domain_event: DomainEvent):
        request_type = type(domain_event)
        if request_type in self._handlers:
            handler:BaseHandler[DomainEvent] = self._handlers[request_type]

            return handler.handle(domain_event)

        raise Exception(f"No handler registered for {request_type}")