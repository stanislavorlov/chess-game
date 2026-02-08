from typing import TypeVar
from ...domain.kernel.base import BaseEvent

T = TypeVar('T', bound=BaseEvent)


class AggregateRoot:

    def __init__(self):
        self._events = []

    @property
    def domain_events(self) -> list:
        return self._events

    def raise_event(self, domain_event: BaseEvent):
        self._events.append(domain_event)

    def raise_events(self, domain_events: list[BaseEvent]):
        self._events.extend(domain_events)