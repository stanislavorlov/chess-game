from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from ...domain.kernel.base import BaseQuery

QT = TypeVar('QT', bound=BaseQuery)
RT = TypeVar('RT')


class BaseQueryHandler(ABC, Generic[QT, RT]):
    @abstractmethod
    async def handle(self, query: QT) -> RT:
        ...