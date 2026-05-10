from dataclasses import dataclass
from enum import IntEnum

class PieceType(IntEnum):
    Pawn = 1
    Knight = 2
    Bishop = 3
    Rook = 4
    Queen = 5
    King = 6

class Side(IntEnum):
    White = 0
    Black = 1

@dataclass
class Bitboards:
    white_pawns: int = 0
    white_knights: int = 0
    white_bishops: int = 0
    white_rooks: int = 0
    white_queens: int = 0
    white_kings: int = 0
    
    black_pawns: int = 0
    black_knights: int = 0
    black_bishops: int = 0
    black_rooks: int = 0
    black_queens: int = 0
    black_kings: int = 0

    def generate_maps(self):
        bb_map = {
            (Side.White, PieceType.Pawn): self.white_pawns,
            (Side.White, PieceType.Knight): self.white_knights,
            (Side.White, PieceType.Bishop): self.white_bishops,
            (Side.White, PieceType.Rook): self.white_rooks,
            (Side.White, PieceType.Queen): self.white_queens,
            (Side.White, PieceType.King): self.white_kings,
            (Side.Black, PieceType.Pawn): self.black_pawns,
            (Side.Black, PieceType.Knight): self.black_knights,
            (Side.Black, PieceType.Bishop): self.black_bishops,
            (Side.Black, PieceType.Rook): self.black_rooks,
            (Side.Black, PieceType.Queen): self.black_queens,
            (Side.Black, PieceType.King): self.black_kings,
        }
        
        occupancies = {
            Side.White: self.white_pawns | self.white_knights | self.white_bishops | self.white_rooks | self.white_queens | self.white_kings,
            Side.Black: self.black_pawns | self.black_knights | self.black_bishops | self.black_rooks | self.black_queens | self.black_kings
        }
        
        combined_occupancy = occupancies[Side.White] | occupancies[Side.Black]
        
        return bb_map, occupancies, combined_occupancy
