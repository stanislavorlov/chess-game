from typing import List
from ...domain.chessboard.file import File
from ...domain.chessboard.position import Position
from ...domain.chessboard.rank import Rank
from ...domain.movements.movement import Movement
from ...domain.pieces.piece_type import PieceType
from ...domain.value_objects.side import Side


def safe_shift(val: int, shift: int) -> int:
    return (val << shift) & 0xFFFFFFFFFFFFFFFF


def set_bit(bitboard: int, index: int) -> int:
    return bitboard | (1 << index)


def clear_bit(bitboard: int, index: int) -> int:
    return bitboard & ~(1 << index)


def get_bit(bitboard: int, index: int) -> bool:
    return bool((bitboard >> index) & 1)


def count_bits(bitboard: int) -> int:
    return bin(bitboard).count('1')


def get_rook_attacks(square: int, occupancy: int) -> int:
    attacks = 0
    rank = square // 8
    file = square % 8

    # North
    for r in range(rank + 1, 8):
        s = r * 8 + file
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    # South
    for r in range(rank - 1, -1, -1):
        s = r * 8 + file
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    # East
    for f in range(file + 1, 8):
        s = rank * 8 + f
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    # West
    for f in range(file - 1, -1, -1):
        s = rank * 8 + f
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    return attacks


def get_bishop_attacks(square: int, occupancy: int) -> int:
    attacks = 0
    rank = square // 8
    file = square % 8

    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, df in directions:
        r, f = rank + dr, file + df
        while 0 <= r < 8 and 0 <= f < 8:
            s = r * 8 + f
            attacks |= (1 << s)
            if occupancy & (1 << s): break
            r, f = r + dr, f + df
    return attacks


def get_queen_attacks(square: int, occupancy: int) -> int:
    return get_rook_attacks(square, occupancy) | get_bishop_attacks(square, occupancy)


class BitboardUtils:
    # File masks
    FILE_A = 0x0101010101010101
    FILE_B = FILE_A << 1
    FILE_C = FILE_A << 2
    FILE_D = FILE_A << 3
    FILE_E = FILE_A << 4
    FILE_F = FILE_A << 5
    FILE_G = FILE_A << 6
    FILE_H = FILE_A << 7

    # Rank masks
    RANK_1 = 0x00000000000000FF
    RANK_2 = RANK_1 << 8
    RANK_3 = RANK_1 << 16
    RANK_4 = RANK_1 << 24
    RANK_5 = RANK_1 << 32
    RANK_6 = RANK_1 << 40
    RANK_7 = RANK_1 << 48
    RANK_8 = RANK_1 << 56

    def __init__(self):
        # Pre-calculated move masks
        self.KNIGHT_MOVES: List[int] = [0] * 64
        self.KING_MOVES: List[int] = [0] * 64
        self.WHITE_PAWN_ATTACKS: List[int] = [0] * 64
        self.BLACK_PAWN_ATTACKS: List[int] = [0] * 64
        self._init_masks()

    def _init_masks(self):
        for i in range(64):
            # Knight Moves
            knight_mask = 0
            # 2 up, 1 left/right
            knight_mask |= safe_shift(1 << i, 17) & ~self.FILE_A
            knight_mask |= safe_shift(1 << i, 15) & ~self.FILE_H
            # 2 down, 1 left/right
            knight_mask |= (1 << i >> 17) & ~self.FILE_H
            knight_mask |= (1 << i >> 15) & ~self.FILE_A
            # 1 up, 2 left/right
            knight_mask |= safe_shift(1 << i, 10) & ~(self.FILE_A | self.FILE_B)
            knight_mask |= safe_shift(1 << i, 6) & ~(self.FILE_G | self.FILE_H)
            # 1 down, 2 left/right
            knight_mask |= (1 << i >> 10) & ~(self.FILE_G | self.FILE_H)
            knight_mask |= (1 << i >> 6) & ~(self.FILE_A | self.FILE_B)
            self.KNIGHT_MOVES[i] = knight_mask

            # King Moves
            king_mask = 0
            king_mask |= safe_shift(1 << i, 1) & ~self.FILE_A
            king_mask |= (1 << i >> 1) & ~self.FILE_H
            king_mask |= safe_shift(1 << i, 8)
            king_mask |= (1 << i >> 8)
            king_mask |= safe_shift(1 << i, 7) & ~self.FILE_H
            king_mask |= safe_shift(1 << i, 9) & ~self.FILE_A
            king_mask |= (1 << i >> 7) & ~self.FILE_A
            king_mask |= (1 << i >> 9) & ~self.FILE_H
            self.KING_MOVES[i] = king_mask

            # White Pawn Attacks (from idx i)
            white_attacks = 0
            if i < 56:
                if not (self.FILE_A & (1 << i)): white_attacks |= (1 << (i + 7))
                if not (self.FILE_H & (1 << i)): white_attacks |= (1 << (i + 9))
            self.WHITE_PAWN_ATTACKS[i] = white_attacks

            # Black Pawn Attacks (from idx i)
            black_attacks = 0
            if i > 7:
                if not (self.FILE_H & (1 << i)): black_attacks |= (1 << (i - 7))
                if not (self.FILE_A & (1 << i)): black_attacks |= (1 << (i - 9))
            self.BLACK_PAWN_ATTACKS[i] = black_attacks


def to_bit_index(position: Position) -> int:
    return (position.rank.value - 1) * 8 + position.file.to_index()


def bit_index_to_position(index: int) -> Position:
    file_idx = index % 8
    rank_idx = (index // 8) + 1
    return Position(File.from_index(file_idx), Rank.from_index(rank_idx))


def bits_to_movements(bitboard: int, from_idx: int = None, from_delta: int = None) -> List[Movement]:
    movements = []
    for i in range(64):
        if (bitboard >> i) & 1:
            to_pos = bit_index_to_position(i)
            idx = from_idx if from_idx is not None else (i + from_delta)
            from_pos = bit_index_to_position(idx)
            movements.append(Movement(from_pos, to_pos))
    return movements


def get_sliding_moves(p_type: PieceType, pieces: int, full_occupancy: int, own_occupancy: int) -> List[Movement]:
    moves = []
    for i in range(64):
        if (pieces >> i) & 1:
            if p_type == PieceType.Rook:
                attacks = get_rook_attacks(i, full_occupancy)
            elif p_type == PieceType.Bishop:
                attacks = get_bishop_attacks(i, full_occupancy)
            elif p_type == PieceType.Queen:
                attacks = get_queen_attacks(i, full_occupancy)
            else:
                continue

            valid_moves = attacks & ~own_occupancy
            moves.extend(bits_to_movements(valid_moves, from_idx=i))
    return moves


def set_piece_bit(bit_index: int, side: Side, piece_type: PieceType, bitboards: dict, occupancy: dict):
    bitboards[(side, piece_type)] = set_bit(bitboards[(side, piece_type)], bit_index)
    occupancy[side] = set_bit(occupancy[side], bit_index)
    occupancy[None] = set_bit(occupancy[None], bit_index)


def clear_piece_bit(bit_index: int, side: Side, piece_type: PieceType, bitboards: dict, occupancy: dict):
    bitboards[(side, piece_type)] = clear_bit(bitboards[(side, piece_type)], bit_index)
    occupancy[side] = clear_bit(occupancy[side], bit_index)
    occupancy[None] = clear_bit(occupancy[None], bit_index)


def get_pawn_moves(side: Side, pawns: int, occupancy_combined: int, occupancy_opponent: int, utils: BitboardUtils) -> List[Movement]:
    moves = []
    empty_squares = ~occupancy_combined
    
    if side == Side.white():
        # Standard push (1 square forward)
        single_push = (pawns << 8) & empty_squares
        # Initial double push (2 squares forward from rank 2)
        double_push = ((pawns & utils.RANK_2) << 8 & empty_squares) << 8 & empty_squares
        
        # Captures
        capture_left = (pawns << 7) & occupancy_opponent & ~utils.FILE_H
        capture_right = (pawns << 9) & occupancy_opponent & ~utils.FILE_A
    else:
        # Standard push (1 square forward)
        single_push = (pawns >> 8) & empty_squares
        # Initial double push (2 squares forward from rank 7)
        double_push = ((pawns & utils.RANK_7) >> 8 & empty_squares) >> 8 & empty_squares
        
        # Captures
        capture_left = (pawns >> 9) & occupancy_opponent & ~utils.FILE_H
        capture_right = (pawns >> 7) & occupancy_opponent & ~utils.FILE_A

    # Convert bitmasks back to Movement objects
    moves.extend(bits_to_movements(single_push, from_delta=-(8 if side == Side.white() else -8)))
    moves.extend(bits_to_movements(double_push, from_delta=-(16 if side == Side.white() else -16)))
    moves.extend(bits_to_movements(capture_left, from_delta=-(7 if side == Side.white() else -9)))
    moves.extend(bits_to_movements(capture_right, from_delta=-(9 if side == Side.white() else -7)))

    return moves


def get_knight_moves(pieces: int, own_occupancy: int, utils: BitboardUtils) -> List[Movement]:
    moves = []
    for i in range(64):
        if (pieces >> i) & 1:
            attacks = utils.KNIGHT_MOVES[i]
            valid_moves = attacks & ~own_occupancy
            moves.extend(bits_to_movements(valid_moves, from_idx=i))
    return moves


def get_king_moves(pieces: int, own_occupancy: int, utils: BitboardUtils) -> List[Movement]:
    moves = []
    for i in range(64):
        if (pieces >> i) & 1:
            attacks = utils.KING_MOVES[i]
            valid_moves = attacks & ~own_occupancy
            moves.extend(bits_to_movements(valid_moves, from_idx=i))
    return moves


def get_castling_moves(
    side: Side, 
    king_pos: Position, 
    king_moved: bool, 
    is_check: bool,
    rook_h_unmoved: bool,
    rook_a_unmoved: bool,
    is_square_occupied_fn, # callback(pos) -> bool
    is_square_attacked_fn, # callback(pos, opponent_side) -> bool
) -> List[Movement]:
    moves = []
    if not king_pos or king_moved or is_check:
        return moves

    rank = Rank.r1() if side == Side.white() else Rank.r8()
    opponent_side = Side.black() if side == Side.white() else Side.white()

    # Kingside
    if rook_h_unmoved:
        f_pos = Position(File.f(), rank)
        g_pos = Position(File.g(), rank)
        if not is_square_occupied_fn(f_pos) and not is_square_occupied_fn(g_pos):
            if not is_square_attacked_fn(f_pos, opponent_side):
                moves.append(Movement(king_pos, g_pos))

    # Queenside
    if rook_a_unmoved:
        d_pos = Position(File.d(), rank)
        c_pos = Position(File.c(), rank)
        b_pos = Position(File.b(), rank)
        if not is_square_occupied_fn(d_pos) and not is_square_occupied_fn(c_pos) and not is_square_occupied_fn(b_pos):
            if not is_square_attacked_fn(d_pos, opponent_side):
                moves.append(Movement(king_pos, c_pos))

    return moves


def get_lsb_index(bitboard: int) -> int:
    if bitboard == 0:
        return -1
    return (bitboard & -bitboard).bit_length() - 1


def is_square_attacked(
    square_index: int,
    attacking_side: Side,
    bitboards: dict,
    occupancy_combined: int,
    utils: BitboardUtils
) -> bool:
    # Attacked by Pawns
    pawns = bitboards.get((attacking_side, PieceType.Pawn), 0)
    if attacking_side == Side.white():
        if utils.BLACK_PAWN_ATTACKS[square_index] & pawns: return True
    else:
        if utils.WHITE_PAWN_ATTACKS[square_index] & pawns: return True

    # Attacked by Knights
    knights = bitboards.get((attacking_side, PieceType.Knight), 0)
    if utils.KNIGHT_MOVES[square_index] & knights: 
        return True
        
    # Attacked by King
    king = bitboards.get((attacking_side, PieceType.King), 0)
    if utils.KING_MOVES[square_index] & king:
        return True
        
    # Attacked by Sliders
    rooks = bitboards.get((attacking_side, PieceType.Rook), 0)
    queens = bitboards.get((attacking_side, PieceType.Queen), 0)
    rooks_queens = rooks | queens
    if get_rook_attacks(square_index, occupancy_combined) & rooks_queens: 
        return True
    
    bishops = bitboards.get((attacking_side, PieceType.Bishop), 0)
    bishops_queens = bishops | queens
    if get_bishop_attacks(square_index, occupancy_combined) & bishops_queens : 
        return True
    
    return False
