from typing import List


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
