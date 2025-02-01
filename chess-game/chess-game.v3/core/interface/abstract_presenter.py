from abc import abstractmethod
from typing import Callable, Any

from core.domain.game.game_state import GameState


class AbstractPresenter:

    @abstractmethod
    def draw(self, state: GameState):
        pass

    @abstractmethod
    def onclick_handler(self, callback: Callable[..., Any]):
        pass
