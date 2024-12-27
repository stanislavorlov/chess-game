# entity

from Model.Kernel.Entity import Entity
from Model.Pieces.Piece import Piece
from Model.ValueObjects.Color import Color
from Model.ValueObjects.Position import Position

class Cell(Entity):
    def __init__(self, position: Position, color: Color):
        self._position = position
        self._color = color
        self._piece = None
        
    def occupy(self, piece: Piece):
        if not self._piece:
            self._piece = piece
    
    def is_occupied(self) -> bool:
        return self._piece != None