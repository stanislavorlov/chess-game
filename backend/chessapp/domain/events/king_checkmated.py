from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent


@dataclass(frozen=True, kw_only=True)
class KingCheckMated(BaseEvent):
    @property
    def event_type(self) -> str:
        return "king-checkmated"
