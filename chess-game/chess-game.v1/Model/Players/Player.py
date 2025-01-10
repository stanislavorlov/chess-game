from Model.Kernel.Entity import Entity
from Model.ValueObjects.Color import Color

class Player(Entity):
    def __init__(self, color: Color):
        self._color = color
        self._pieces = []