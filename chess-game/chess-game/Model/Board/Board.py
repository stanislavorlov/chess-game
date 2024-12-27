from collections import defaultdict
from typing import TypedDict
from Model.Board.Cell import Cell
from Model.Kernel.Entity import Entity
from Model.Pieces.Piece import Piece
from Model.ValueObjects.Color import Color
from Model.ValueObjects.Position import Position

class Board(Entity):
    
    FILES = "abcdefgh"
    RANKS = "12345678"
    
    def __init__(self):
        self._init_board()
        
    def _init_board(self):
        self._cells = TypedDict('Cell', {})
        # for 2 players only
        for fileIdx, file in enumerate(self.FILES):
            for rankIdx, rank in enumerate(self.RANKS):
                position = Position(file, rank)
                self._cells[str(position)] = Cell(position, self.__get_color(fileIdx, rankIdx))

        return self._cells
    
    def __get_color(self, file, rank):
        return Color.BLACK if (file + rank) % 2 == 0 else Color.WHITE
    
    def place_piece(self, piece: Piece, position: Position):
        if position.file in self.FILES and position.rank in self.RANKS:
            cell: Cell = self._cells[str(position)]
            if not cell.is_occupied():
                cell.occupy(piece)
            else:
                print('check if enemy piece than take it and than occupy the cell')