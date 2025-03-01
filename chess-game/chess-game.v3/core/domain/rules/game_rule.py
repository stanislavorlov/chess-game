from abc import abstractmethod

from core.domain.kernel.entity import Entity


class GameRule(Entity):

    def __init__(self):
        super().__init__()
