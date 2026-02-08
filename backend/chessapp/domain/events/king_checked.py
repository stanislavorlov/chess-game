from dataclasses import dataclass
from ...domain.kernel.base import BaseEvent


@dataclass(frozen=True, kw_only=True)
class KingChecked(BaseEvent):
    @property
    def event_type(self) -> str:
        return "king-checked"