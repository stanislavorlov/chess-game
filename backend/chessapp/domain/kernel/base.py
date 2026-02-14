from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...

@dataclass(frozen=True, eq=False)
class BaseQuery(ABC):
    ...

@dataclass(frozen=True, eq=False)
class BaseEvent(ABC):
    @property
    @abstractmethod
    def event_type(self) -> str:
        ...

    def to_dict(self) -> dict:
        from .serialization import domain_to_dict
        result = domain_to_dict(self)
        result["event_type"] = self.event_type
        return result

@dataclass(frozen=True, eq=False)
class BaseResponse(ABC):
    ...