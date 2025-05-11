from typing import TypeVar
from diator.events import DomainEvent

T = TypeVar('T', bound=DomainEvent)

class Entity:

    def __init__(self):
        self._events = []

    @property
    def domain_events(self) -> list:
        return self._events

    def raise_event(self, domain_event: DomainEvent):
        self._events.append(domain_event)

    def raise_events(self, domain_events: list[DomainEvent]):
        self._events.extend(domain_events)