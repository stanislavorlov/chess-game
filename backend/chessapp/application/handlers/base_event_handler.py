from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from ...domain.kernel.base import BaseEvent

ET = TypeVar('ET', bound=BaseEvent)
RT = TypeVar('RT')


class BaseEventHandler(ABC, Generic[ET, RT]):
    @abstractmethod
    async def handle(self, event: ET) -> RT:
        ...