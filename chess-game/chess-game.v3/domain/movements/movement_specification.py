from domain.pieces.piece import Piece

class MovementSpecification:

    def is_satisfiedby(self, piece: Piece) -> bool:
        # track changes between start and destination position

        # pawn: only changes in rank by 1 or 2
        # knight: 1 rank and 2 files OR 2 ranks and 1 file
        # bishop: rank changes == file changes
        # rock: only rank changes OR only file changes


        return False