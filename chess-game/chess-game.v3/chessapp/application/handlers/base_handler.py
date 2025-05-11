from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T", bound="DomainEvent")

class BaseHandler(ABC, Generic[T]):

    @abstractmethod
    def handle(self, event: T):
        pass