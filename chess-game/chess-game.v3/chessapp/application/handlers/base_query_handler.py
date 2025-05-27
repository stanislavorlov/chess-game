from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from chessapp.domain.kernel.base import BaseQuery

QT = TypeVar('QT', bound=BaseQuery)
RT = TypeVar('RT')


@dataclass(frozen=True, eq=False)
class BaseQueryHandler(ABC, Generic[QT, RT]):
    @abstractmethod
    async def handle(self, query: QT) -> RT:
        ...