# Entity

from Model.Pieces.Piece import Piece
from Model.ValueObjects.Position import Position

class Pawn(Piece):
    def __init__(self, id, color, position):
        super().__init__(id, color, position)
        self.has_moved = False
        
    def move(self, new_position):
        if not isinstance(new_position, Position):
            raise ValueError("new_position must be a Position object.")
        
        if new_position.file == self._position.file and new_position.rank == self._position.rank + 1:
            super().move(new_position)
            self.has_moved = True
        
    def promote(self, new_piece_type):
        # ToDo: promote logic
        pass