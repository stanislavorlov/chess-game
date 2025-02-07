from typing import TypeVar
from diator.events import DomainEvent

T = TypeVar('T', bound=DomainEvent)


class AggregateRoot:

    def __init__(self):
        self._events = []

    @property
    def domain_events(self) -> list:
        return self._events

    def raise_event(self, domain_event: T):
        self._events.append(domain_event)