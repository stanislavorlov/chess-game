from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...

@dataclass(frozen=True, eq=False)
class BaseQuery(ABC):
    ...

@dataclass(frozen=True, eq=False)
class BaseEvent(ABC):
    ...

@dataclass(frozen=True, eq=False)
class BaseResponse(ABC):
    ...