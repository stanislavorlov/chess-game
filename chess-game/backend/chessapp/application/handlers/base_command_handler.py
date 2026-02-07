from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from chessapp.domain.kernel.base import BaseCommand

CT = TypeVar('CT', bound=BaseCommand)
RT = TypeVar('RT')


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CT, RT]):
    @abstractmethod
    async def handle(self, command: CT) -> RT:
        if not isinstance(command, CT.__bound__):
            raise Exception(f'Invalid command type: {type(command)} of {self.__class__}')
        ...