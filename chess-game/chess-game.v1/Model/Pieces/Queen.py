from Model.Pieces.Piece import Piece
from Model.ValueObjects.Color import Color
from Model.ValueObjects.Position import Position

class Queen(Piece):
    def __init__(self, id, color: Color, position: Position):
        super().__init__(id, color, position)