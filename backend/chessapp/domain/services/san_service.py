from ..chessboard.board import Board
from ..pieces.piece_type import PieceType
from ..events.king_castled import KingCastled
from ..events.piece_moved import PieceMoved
from ..value_objects.san import SAN

class SanService:
    @staticmethod
    def calculate(event, board_before_move: Board) -> SAN:
        """
        Calculates Standard Algebraic Notation for a given move event.
        Relocated from SAN.from_move to decouple value objects from complex logic.
        """
        if isinstance(event, KingCastled):
            return SAN("O-O" if event.is_kingside else "O-O-O")

        if isinstance(event, PieceMoved):
            piece = event.piece
            from_ = event.from_
            to = event.to
            piece_type = piece.get_piece_type()
            
            # Castling check (standard representation if not captured by KingCastled)
            if piece_type == PieceType.King and abs(to.file.to_index() - from_.file.to_index()) == 2:
                return SAN("O-O" if to.file.to_index() > from_.file.to_index() else "O-O-O")

            san_str = ""
            if piece_type != PieceType.Pawn:
                san_str += piece_type.value
            
            # Disambiguation
            if piece_type != PieceType.Pawn:
                others = []
                for pos in board_before_move:
                    sq = board_before_move[pos]
                    if sq.piece and sq.piece.get_side() == piece.get_side() and \
                       sq.piece.get_piece_type() == piece_type and pos != from_:
                        
                        moves = board_before_move.get_legal_moves(piece.get_side())
                        can_reach = any(m.from_position == pos and m.to_position == to for m in moves)
                        if can_reach:
                            others.append(pos)
                
                if others:
                    same_file = any(o.file == from_.file for o in others)
                    same_rank = any(o.rank == from_.rank for o in others)
                    
                    if not same_file:
                        san_str += str(from_.file)
                    elif not same_rank:
                        san_str += str(from_.rank)
                    else:
                        san_str += str(from_.file) + str(from_.rank)

            is_capture = board_before_move[to].piece is not None
            if is_capture:
                if piece_type == PieceType.Pawn:
                    san_str += str(from_.file)
                san_str += "x"
            
            san_str += str(to)
            return SAN(san_str)

        raise ValueError(f"Unsupported event type for SAN parsing: {type(event)}")
