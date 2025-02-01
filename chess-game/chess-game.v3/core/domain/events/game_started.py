from dataclasses import dataclass

from diator.events import DomainEvent


@dataclass(frozen=True, kw_only=True)
class GameStartedEvent(DomainEvent):
    pass