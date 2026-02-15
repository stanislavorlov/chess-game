from typing import List, Optional
from ..pieces.piece import Piece
from ..pieces.piece_type import PieceType
from ...domain.chessboard.file import File
from ...domain.chessboard.position import Position
from ...domain.chessboard.rank import Rank
from ...domain.chessboard.square import Square
from ...domain.events.king_checked import KingChecked
from ...domain.events.king_checkmated import KingCheckMated
from ...domain.events.pawn_promoted import PawnPromoted
from ...domain.events.piece_captured import PieceCaptured
from ...domain.events.piece_moved import PieceMoved
from ...domain.kernel.value_object import ValueObject
from ...domain.movements.movement import Movement
from ...domain.pieces.bishop import Bishop
from ...domain.pieces.king import King
from ...domain.pieces.knight import Knight
from ...domain.pieces.pawn import Pawn
from ...domain.pieces.queen import Queen
from ...domain.pieces.rook import Rook
from ...domain.value_objects.side import Side
from .bitboard_utils import BitboardUtils, set_bit, clear_bit, get_rook_attacks, get_bishop_attacks, get_queen_attacks, \
    count_bits


def _to_bit_index(position: Position) -> int:
    return (position.rank.value - 1) * 8 + position.file.to_index()


def _bit_index_to_position(index: int) -> Position:
    file_idx = index % 8
    rank_idx = (index // 8) + 1
    return Position(File.from_index(file_idx), Rank.from_index(rank_idx))


class Board(ValueObject):

    def __init__(self):
        super().__init__()
        self._bitboard_utils = BitboardUtils()
        self._board: dict[Position, Square] = {}
        # 12 bitboards for each piece type and color
        self._bitboards: dict[tuple[Side, PieceType], int] = {}
        # 3 occupancy bitboards: white, black, and combined
        self._occupancy: dict[Optional[Side], int] = {
            Side.white(): 0,
            Side.black(): 0,
            None: 0
        }
        self.__initialize_bitboards()
        self.__board_initialize__(self._board)

    def __initialize_bitboards(self):
        for side in [Side.white(), Side.black()]:
            for piece_type in PieceType:
                self._bitboards[(side, piece_type)] = 0

    def _set_piece_bit(self, position: Position, piece: Piece):
        bit_index = _to_bit_index(position)
        side = piece.get_side()
        piece_type = piece.get_piece_type()

        self._bitboards[(side, piece_type)] = set_bit(self._bitboards[(side, piece_type)], bit_index)
        self._occupancy[side] = set_bit(self._occupancy[side], bit_index)
        self._occupancy[None] = set_bit(self._occupancy[None], bit_index)

    def _clear_piece_bit(self, position: Position, piece: Piece):
        bit_index = _to_bit_index(position)
        side = piece.get_side()
        piece_type = piece.get_piece_type()

        self._bitboards[(side, piece_type)] = clear_bit(self._bitboards[(side, piece_type)], bit_index)
        self._occupancy[side] = clear_bit(self._occupancy[side], bit_index)
        self._occupancy[None] = clear_bit(self._occupancy[None], bit_index)

    def piece_moved(self, piece_moved: PieceMoved):
        piece = piece_moved.piece
        from_ = piece_moved.from_
        to = piece_moved.to

        # Update dictionary-based board
        self._board[from_] = Square(from_, None)
        self._board[to] = Square(to, piece)

        # Update bitboards
        self._clear_piece_bit(from_, piece)
        self._set_piece_bit(to, piece)

    def piece_captured(self, piece_captured: PieceCaptured):
        # The PieceMoved event following this will update the square piece on 'to' position.
        # But we must clear the bit of the captured piece first.
        self._clear_piece_bit(piece_captured.to, piece_captured.piece)
        pass

    def pawn_promoted(self, pawn_promoted: PawnPromoted):
        pass

    def king_checked(self, king_checked: KingChecked):
        pass

    def king_checkmated(self, king_checkmated: KingCheckMated):
        pass

    def search_available_moves(self) -> List[Movement]:
        list_of_moves = []
        
        for side in [Side.white(), Side.black()]:
            # Pawns
            list_of_moves.extend(self._get_pawn_moves(side))
            # Knights
            list_of_moves.extend(self._get_knight_moves(side))
            # Kings
            list_of_moves.extend(self._get_king_moves(side))
            # Sliders
            list_of_moves.extend(self._get_sliding_moves(side, PieceType.Rook))
            list_of_moves.extend(self._get_sliding_moves(side, PieceType.Bishop))
            list_of_moves.extend(self._get_sliding_moves(side, PieceType.Queen))

        return list_of_moves

    def _get_pawn_moves(self, side: Side) -> List[Movement]:
        moves = []
        pawns = self._bitboards[(side, PieceType.Pawn)]
        empty_squares = ~self._occupancy[None]
        opponent_occupancy = self._occupancy[Side.black() if side == Side.white() else Side.white()]
        
        if side == Side.white():
            # Standard push (1 square forward)
            single_push = (pawns << 8) & empty_squares
            # Initial double push (2 squares forward from rank 2)
            # Both the intermediate (rank 3) and target (rank 4) squares must be empty
            double_push = ((pawns & self._bitboard_utils.RANK_2) << 8 & empty_squares) << 8 & empty_squares
            
            # Captures
            capture_left = (pawns << 7) & opponent_occupancy & ~self._bitboard_utils.FILE_H
            capture_right = (pawns << 9) & opponent_occupancy & ~self._bitboard_utils.FILE_A
        else:
            # Standard push (1 square forward)
            single_push = (pawns >> 8) & empty_squares
            # Initial double push (2 squares forward from rank 7)
            # Both the intermediate (rank 6) and target (rank 5) squares must be empty
            double_push = ((pawns & self._bitboard_utils.RANK_7) >> 8 & empty_squares) >> 8 & empty_squares
            
            # Captures
            capture_left = (pawns >> 9) & opponent_occupancy & ~self._bitboard_utils.FILE_H
            capture_right = (pawns >> 7) & opponent_occupancy & ~self._bitboard_utils.FILE_A
 
        # Convert bitmasks back to Movement objects
        moves.extend(self._bits_to_movements(single_push, from_delta=-(8 if side == Side.white() else -8)))
        moves.extend(self._bits_to_movements(double_push, from_delta=-(16 if side == Side.white() else -16)))
        moves.extend(self._bits_to_movements(capture_left, from_delta=-(7 if side == Side.white() else -9)))
        moves.extend(self._bits_to_movements(capture_right, from_delta=-(9 if side == Side.white() else -7)))

        return moves

    def _get_knight_moves(self, side: Side) -> List[Movement]:
        moves = []
        pieces = self._bitboards[(side, PieceType.Knight)]
        own_occupancy = self._occupancy[side]
        for i in range(64):
            if (pieces >> i) & 1:
                attacks = self._bitboard_utils.KNIGHT_MOVES[i]
                valid_moves = attacks & ~own_occupancy
                moves.extend(self._bits_to_movements(valid_moves, from_idx=i))
        return moves

    def _get_king_moves(self, side: Side) -> List[Movement]:
        moves = []
        pieces = self._bitboards[(side, PieceType.King)]
        own_occupancy = self._occupancy[side]
        for i in range(64):
            if (pieces >> i) & 1:
                attacks = self._bitboard_utils.KING_MOVES[i]
                valid_moves = attacks & ~own_occupancy
                moves.extend(self._bits_to_movements(valid_moves, from_idx=i))
        return moves

    def _get_sliding_moves(self, side: Side, p_type: PieceType) -> List[Movement]:
        moves = []
        pieces = self._bitboards[(side, p_type)]
        full_occupancy = self._occupancy[None]
        own_occupancy = self._occupancy[side]
        
        for i in range(64):
            if (pieces >> i) & 1:
                if p_type == PieceType.Rook:
                    attacks = get_rook_attacks(i, full_occupancy)
                elif p_type == PieceType.Bishop:
                    attacks = get_bishop_attacks(i, full_occupancy)
                elif p_type == PieceType.Queen:
                    attacks = get_queen_attacks(i, full_occupancy)
                else: continue
                
                valid_moves = attacks & ~own_occupancy
                moves.extend(self._bits_to_movements(valid_moves, from_idx=i))
        return moves

    def _bits_to_movements(self, bitboard: int, from_idx: int = None, from_delta: int = None) -> List[Movement]:
        movements = []
        for i in range(64):
            if (bitboard >> i) & 1:
                to_pos = _bit_index_to_position(i)
                idx = from_idx if from_idx is not None else (i + from_delta)
                from_pos = _bit_index_to_position(idx)
                movements.append(Movement(from_pos, to_pos))
        return movements

    def evaluate_board(self) -> float:
        """Basic evaluation based on material weight."""
        score = 0
        weights = {
            PieceType.Pawn: 10,
            PieceType.Knight: 30,
            PieceType.Bishop: 30,
            PieceType.Rook: 50,
            PieceType.Queen: 90,
            PieceType.King: 900
        }
        
        for (side, p_type), bb in self._bitboards.items():
            count = count_bits(bb)
            val = count * weights[p_type]
            score += val if side == Side.white() else -val
            
        return score

    def is_check(self, side: Side) -> bool:
        king_bb = self._bitboards[(side, PieceType.King)]
        if king_bb == 0: return False
        
        # Get index of the set bit
        king_idx = (king_bb & -king_bb).bit_length() - 1
        king_pos = _bit_index_to_position(king_idx)
        opponent_side = Side.black() if side == Side.white() else Side.white()
        
        return self.is_attacked(king_pos, opponent_side)

    def is_attacked(self, position: Position, attacking_side: Side) -> bool:
        idx = _to_bit_index(position)
        full_occ = self._occupancy[None]
        
        # Attacked by Pawns
        pawns = self._bitboards[(attacking_side, PieceType.Pawn)]
        if attacking_side == Side.white():
            if self._bitboard_utils.BLACK_PAWN_ATTACKS[idx] & pawns: return True
        else:
            if self._bitboard_utils.WHITE_PAWN_ATTACKS[idx] & pawns: return True

        # Attacked by Knights
        if self._bitboard_utils.KNIGHT_MOVES[idx] & self._bitboards[(attacking_side, PieceType.Knight)]: 
            return True
        # Attacked by King
        if self._bitboard_utils.KING_MOVES[idx] & self._bitboards[(attacking_side, PieceType.King)]:
            return True
        # Attacked by Sliders
        rooks_queens = self._bitboards[(attacking_side, PieceType.Rook)] | self._bitboards[(attacking_side, PieceType.Queen)]
        if get_rook_attacks(idx, full_occ) & rooks_queens: return True
        
        bishops_queens = self._bitboards[(attacking_side, PieceType.Bishop)] | self._bitboards[(attacking_side, PieceType.Queen)]
        if get_bishop_attacks(idx, full_occ) & bishops_queens : return True
        
        return False

    def clone(self):
        new_board = Board.__new__(Board)
        new_board._bitboard_utils = self._bitboard_utils
        new_board._board = self._board.copy()
        new_board._bitboards = self._bitboards.copy()
        new_board._occupancy = self._occupancy.copy()
        return new_board

    def get_legal_moves(self, side: Side) -> List[Movement]:
        pseudo_legal_moves = self.search_available_moves()
        # Filter for current turn's pieces
        side_pseudo = [m for m in pseudo_legal_moves if self._board[m.from_position].piece.get_side() == side]
        
        legal_moves = []
        for move in side_pseudo:
            temp_board = self.clone()
            
            # Simulate capture if necessary
            target_piece = temp_board._board[move.to_position].piece
            if target_piece:
                temp_board.piece_captured(PieceCaptured(game_id=None, from_=move.from_position, to=move.to_position, piece=target_piece))
            
            # Simulate move
            moving_piece = temp_board._board[move.from_position].piece
            temp_board.piece_moved(PieceMoved(game_id=None, from_=move.from_position, to=move.to_position, piece=moving_piece))
            
            if not temp_board.is_check(side):
                legal_moves.append(move)
        return legal_moves

    def is_checkmate(self, side: Side) -> bool:
        return self.is_check(side) and len(self.get_legal_moves(side)) == 0

    def __board_initialize__(self, board: dict[Position, Square]):
        for file in File.a():
            for rank in Rank.r1():
                piece_color = Side.white() if rank in (Rank.r1(), Rank.r2()) else Side.black()
                position = Position(file, rank)
                piece = None

                if rank in (Rank.r2(), Rank.r7()):
                    piece = Pawn(piece_color)
                elif rank in (Rank.r1(), Rank.r8()):
                    if file in (File.a(), File.h()):
                        piece = Rook(piece_color)
                    elif file in (File.b(), File.g()):
                        piece = Knight(piece_color)
                    elif file in (File.c(), File.f()):
                        piece = Bishop(piece_color)
                    elif file == File.d():
                        piece = Queen(piece_color)
                    elif file == File.e():
                        piece = King(piece_color)
                
                board[position] = Square(position, piece)
                if piece:
                  self._set_piece_bit(position, piece)

    def __iter__(self):
        return iter(self._board)

    def __getitem__(self, item: Position):
        return self._board[item]