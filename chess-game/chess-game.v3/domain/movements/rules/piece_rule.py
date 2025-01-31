from abc import ABC, abstractmethod
from domain.movements.movement_intent import MovementIntent

class PieceRule(ABC):

    @abstractmethod
    def is_valid(self, movement_intent: MovementIntent):
        pass