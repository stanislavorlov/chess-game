from ..chessboard.board import Board
from ..value_objects.side import Side

class FenService:
    @staticmethod
    def generate(board: Board) -> str:
        from ..chessboard.file import File
        from ..chessboard.rank import Rank
        from ..chessboard.position import Position

        fen_rows = []
        # FEN needs ranks from 8 to 1
        for rank in reversed(Rank(1)):
            row_str = ""
            empty_count = 0
            # File iterator yields File('a') to File('h')
            for file in File.a():
                pos = Position(file, rank)
                square = board[pos]
                
                if not square.is_occupied:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    
                    piece = square.piece
                    # Standard FEN: uppercase for white, lowercase for black
                    char = piece.get_piece_type().value
                    if piece.get_side() == Side.white():
                        row_str += char.upper()
                    else:
                        row_str += char.lower()
            
            if empty_count > 0:
                row_str += str(empty_count)
            
            fen_rows.append(row_str)
        
        return "/".join(fen_rows)
