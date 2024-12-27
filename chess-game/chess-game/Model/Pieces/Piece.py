# Entity base class

from Model.Kernel.Entity import Entity
from Model.ValueObjects.Color import Color
from Model.ValueObjects.Position import Position

class Piece(Entity):
    
    def __init__(self, id, color: Color, position: Position):
        self._id = id
        self._color = color
        self._position = position
        
    def move(self, new_position: Position):
        self._position = new_position

    def __eq__(self, other):
        return self.id == other.id  # Equality based on unique identity

    def __str__(self):
        return f"{self.color.capitalize()} Pawn at {self.position}"