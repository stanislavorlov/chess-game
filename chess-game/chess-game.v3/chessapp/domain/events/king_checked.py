from dataclasses import dataclass
from diator.events import DomainEvent


@dataclass(frozen=True, kw_only=True)
class KingChecked(DomainEvent):
    pass