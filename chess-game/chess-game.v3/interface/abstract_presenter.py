from abc import abstractmethod

from domain.game_state import GameState

class AbstractPresenter:

    @abstractmethod
    def draw(self, state: GameState):
        pass

    @abstractmethod
    def onclick_handler(self, callback):
        pass
