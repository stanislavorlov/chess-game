from typing import List, Tuple
from .bitboards import Side, PieceType

def safe_shift(val: int, shift: int) -> int:
    if shift >= 64 or shift <= -64:
        return 0
    if shift > 0:
        return (val << shift) & 0xFFFFFFFFFFFFFFFF
    else:
        return val >> (-shift)

def get_rook_attacks(square: int, occupancy: int) -> int:
    attacks = 0
    rank = square // 8
    file = square % 8

    for r in range(rank + 1, 8):
        s = r * 8 + file
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    for r in range(rank - 1, -1, -1):
        s = r * 8 + file
        attacks |= (1 << s)
        if occupancy & (1 << s): break
    for f in range(file + 1, 8):
        s = rank * 8 + f
        attacks |= (1 << s)
        if occupancy & (1 << s): break
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
    FILE_A = 0x0101010101010101
    FILE_B = FILE_A << 1
    FILE_C = FILE_A << 2
    FILE_D = FILE_A << 3
    FILE_E = FILE_A << 4
    FILE_F = FILE_A << 5
    FILE_G = FILE_A << 6
    FILE_H = FILE_A << 7

    RANK_1 = 0x00000000000000FF
    RANK_2 = RANK_1 << 8
    RANK_3 = RANK_1 << 16
    RANK_4 = RANK_1 << 24
    RANK_5 = RANK_1 << 32
    RANK_6 = RANK_1 << 40
    RANK_7 = RANK_1 << 48
    RANK_8 = RANK_1 << 56

    def __init__(self):
        self.KNIGHT_MOVES = [0] * 64
        self.KING_MOVES = [0] * 64
        self.WHITE_PAWN_ATTACKS = [0] * 64
        self.BLACK_PAWN_ATTACKS = [0] * 64
        self._init_masks()

    def _init_masks(self):
        for i in range(64):
            knight_mask = 0
            knight_mask |= safe_shift(1 << i, 17) & ~self.FILE_A
            knight_mask |= safe_shift(1 << i, 15) & ~self.FILE_H
            knight_mask |= safe_shift(1 << i, -17) & ~self.FILE_H
            knight_mask |= safe_shift(1 << i, -15) & ~self.FILE_A
            knight_mask |= safe_shift(1 << i, 10) & ~(self.FILE_A | self.FILE_B)
            knight_mask |= safe_shift(1 << i, 6) & ~(self.FILE_G | self.FILE_H)
            knight_mask |= safe_shift(1 << i, -10) & ~(self.FILE_G | self.FILE_H)
            knight_mask |= safe_shift(1 << i, -6) & ~(self.FILE_A | self.FILE_B)
            self.KNIGHT_MOVES[i] = knight_mask

            king_mask = 0
            king_mask |= safe_shift(1 << i, 1) & ~self.FILE_A
            king_mask |= safe_shift(1 << i, -1) & ~self.FILE_H
            king_mask |= safe_shift(1 << i, 8)
            king_mask |= safe_shift(1 << i, -8)
            king_mask |= safe_shift(1 << i, 7) & ~self.FILE_H
            king_mask |= safe_shift(1 << i, 9) & ~self.FILE_A
            king_mask |= safe_shift(1 << i, -7) & ~self.FILE_A
            king_mask |= safe_shift(1 << i, -9) & ~self.FILE_H
            self.KING_MOVES[i] = king_mask

            white_attacks = 0
            if i < 56:
                if not (self.FILE_A & (1 << i)): white_attacks |= (1 << (i + 7))
                if not (self.FILE_H & (1 << i)): white_attacks |= (1 << (i + 9))
            self.WHITE_PAWN_ATTACKS[i] = white_attacks

            black_attacks = 0
            if i > 7:
                if not (self.FILE_H & (1 << i)): black_attacks |= (1 << (i - 7))
                if not (self.FILE_A & (1 << i)): black_attacks |= (1 << (i - 9))
            self.BLACK_PAWN_ATTACKS[i] = black_attacks

def bits_to_moves(bitboard: int, from_idx: int = None, from_delta: int = None) -> List[Tuple[int, int]]:
    moves = []
    for i in range(64):
        if (bitboard >> i) & 1:
            idx = from_idx if from_idx is not None else (i + from_delta)
            moves.append((idx, i))
    return moves

def get_sliding_moves(p_type: PieceType, pieces: int, full_occupancy: int, own_occupancy: int) -> List[Tuple[int, int]]:
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
            moves.extend(bits_to_moves(valid_moves, from_idx=i))
    return moves

def get_pawn_moves(side: Side, pawns: int, occupancy_combined: int, occupancy_opponent: int, utils: BitboardUtils) -> List[Tuple[int, int]]:
    moves = []
    empty_squares = (~occupancy_combined) & 0xFFFFFFFFFFFFFFFF
    
    if side == Side.White:
        single_push = (pawns << 8) & empty_squares
        double_push = ((pawns & utils.RANK_2) << 8 & empty_squares) << 8 & empty_squares
        capture_left = (pawns << 7) & occupancy_opponent & ~utils.FILE_H
        capture_right = (pawns << 9) & occupancy_opponent & ~utils.FILE_A
    else:
        single_push = (pawns >> 8) & empty_squares
        double_push = ((pawns & utils.RANK_7) >> 8 & emptySquares) >> 8 & emptySquares
        capture_left = (pawns >> 9) & occupancy_opponent & ~utils.FILE_H
        capture_right = (pawns >> 7) & occupancy_opponent & ~utils.FILE_A

    moves.extend(bits_to_moves(single_push, from_delta=-(8 if side == Side.White else -8)))
    moves.extend(bits_to_moves(double_push, from_delta=-(16 if side == Side.White else -16)))
    moves.extend(bits_to_moves(capture_left, from_delta=-(7 if side == Side.White else -9)))
    moves.extend(bits_to_moves(capture_right, from_delta=-(9 if side == Side.White else -7)))
    return moves

def get_knight_moves(pieces: int, own_occupancy: int, utils: BitboardUtils) -> List[Tuple[int, int]]:
    moves = []
    for i in range(64):
        if (pieces >> i) & 1:
            attacks = utils.KNIGHT_MOVES[i]
            valid_moves = attacks & ~own_occupancy
            moves.extend(bits_to_moves(valid_moves, from_idx=i))
    return moves

def get_king_moves(pieces: int, own_occupancy: int, utils: BitboardUtils) -> List[Tuple[int, int]]:
    moves = []
    for i in range(64):
        if (pieces >> i) & 1:
            attacks = utils.KING_MOVES[i]
            valid_moves = attacks & ~own_occupancy
            moves.extend(bits_to_moves(valid_moves, from_idx=i))
    return moves

def get_lsb_index(bitboard: int) -> int:
    if bitboard == 0:
        return -1
    return (bitboard & -bitboard).bit_length() - 1

def is_square_attacked(
    square_index: int,
    attacking_side: Side,
    bb_map: dict,
    occupancy_combined: int,
    utils: BitboardUtils
) -> bool:
    pawns = bb_map.get((attacking_side, PieceType.Pawn), 0)
    if attacking_side == Side.White:
        if utils.BLACK_PAWN_ATTACKS[square_index] & pawns: return True
    else:
        if utils.WHITE_PAWN_ATTACKS[square_index] & pawns: return True

    knights = bb_map.get((attacking_side, PieceType.Knight), 0)
    if utils.KNIGHT_MOVES[square_index] & knights: return True
        
    king = bb_map.get((attacking_side, PieceType.King), 0)
    if utils.KING_MOVES[square_index] & king: return True
        
    rooks_queens = bb_map.get((attacking_side, PieceType.Rook), 0) | bb_map.get((attacking_side, PieceType.Queen), 0)
    if get_rook_attacks(square_index, occupancy_combined) & rooks_queens: return True
    
    bishops_queens = bb_map.get((attacking_side, PieceType.Bishop), 0) | bb_map.get((attacking_side, PieceType.Queen), 0)
    if get_bishop_attacks(square_index, occupancy_combined) & bishops_queens : return True
    
    return False
