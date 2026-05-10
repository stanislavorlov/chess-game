from .bitboards import Bitboards

def count_bits(bitboard: int) -> int:
    return bin(bitboard).count('1')

def evaluate_board(bb: Bitboards) -> float:
    score = 0
    PAWN_WEIGHT = 10
    KNIGHT_WEIGHT = 30
    BISHOP_WEIGHT = 30
    ROOK_WEIGHT = 50
    QUEEN_WEIGHT = 90
    KING_WEIGHT = 900
    
    score += count_bits(bb.white_pawns) * PAWN_WEIGHT
    score += count_bits(bb.white_knights) * KNIGHT_WEIGHT
    score += count_bits(bb.white_bishops) * BISHOP_WEIGHT
    score += count_bits(bb.white_rooks) * ROOK_WEIGHT
    score += count_bits(bb.white_queens) * QUEEN_WEIGHT
    score += count_bits(bb.white_kings) * KING_WEIGHT
    
    score -= count_bits(bb.black_pawns) * PAWN_WEIGHT
    score -= count_bits(bb.black_knights) * KNIGHT_WEIGHT
    score -= count_bits(bb.black_bishops) * BISHOP_WEIGHT
    score -= count_bits(bb.black_rooks) * ROOK_WEIGHT
    score -= count_bits(bb.black_queens) * QUEEN_WEIGHT
    score -= count_bits(bb.black_kings) * KING_WEIGHT
    
    return float(score)
