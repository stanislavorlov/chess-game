from typing import List, Tuple
from .bitboards import Bitboards, Side, PieceType
from . import bitboard_utils as utils

def clone_and_apply_move(bb: Bitboards, from_idx: int, to_idx: int) -> Bitboards:
    new_bb = Bitboards(
        white_pawns=bb.white_pawns,
        white_knights=bb.white_knights,
        white_bishops=bb.white_bishops,
        white_rooks=bb.white_rooks,
        white_queens=bb.white_queens,
        white_kings=bb.white_kings,
        black_pawns=bb.black_pawns,
        black_knights=bb.black_knights,
        black_bishops=bb.black_bishops,
        black_rooks=bb.black_rooks,
        black_queens=bb.black_queens,
        black_kings=bb.black_kings
    )

    from_mask = (1 << from_idx)
    to_mask = (1 << to_idx)
    clear_mask = (~to_mask) & 0xFFFFFFFFFFFFFFFF

    new_bb.white_pawns &= clear_mask
    new_bb.white_knights &= clear_mask
    new_bb.white_bishops &= clear_mask
    new_bb.white_rooks &= clear_mask
    new_bb.white_queens &= clear_mask
    new_bb.white_kings &= clear_mask
    
    new_bb.black_pawns &= clear_mask
    new_bb.black_knights &= clear_mask
    new_bb.black_bishops &= clear_mask
    new_bb.black_rooks &= clear_mask
    new_bb.black_queens &= clear_mask
    new_bb.black_kings &= clear_mask

    if new_bb.white_pawns & from_mask: new_bb.white_pawns = (new_bb.white_pawns & ~from_mask) | to_mask
    if new_bb.white_knights & from_mask: new_bb.white_knights = (new_bb.white_knights & ~from_mask) | to_mask
    if new_bb.white_bishops & from_mask: new_bb.white_bishops = (new_bb.white_bishops & ~from_mask) | to_mask
    if new_bb.white_rooks & from_mask: new_bb.white_rooks = (new_bb.white_rooks & ~from_mask) | to_mask
    if new_bb.white_queens & from_mask: new_bb.white_queens = (new_bb.white_queens & ~from_mask) | to_mask
    if new_bb.white_kings & from_mask: new_bb.white_kings = (new_bb.white_kings & ~from_mask) | to_mask
        
    if new_bb.black_pawns & from_mask: new_bb.black_pawns = (new_bb.black_pawns & ~from_mask) | to_mask
    if new_bb.black_knights & from_mask: new_bb.black_knights = (new_bb.black_knights & ~from_mask) | to_mask
    if new_bb.black_bishops & from_mask: new_bb.black_bishops = (new_bb.black_bishops & ~from_mask) | to_mask
    if new_bb.black_rooks & from_mask: new_bb.black_rooks = (new_bb.black_rooks & ~from_mask) | to_mask
    if new_bb.black_queens & from_mask: new_bb.black_queens = (new_bb.black_queens & ~from_mask) | to_mask
    if new_bb.black_kings & from_mask: new_bb.black_kings = (new_bb.black_kings & ~from_mask) | to_mask

    return new_bb

def get_legal_moves(bb: Bitboards, turn: Side, bitboard_utils: utils.BitboardUtils) -> List[Tuple[int, int]]:
    bb_map, occupancies, combined_occupancy = bb.generate_maps()
    enemy_side = Side.Black if turn == Side.White else Side.White

    moves = []

    for i in range(64):
        p_type = None
        for pt in [PieceType.Pawn, PieceType.Knight, PieceType.Bishop, PieceType.Rook, PieceType.Queen, PieceType.King]:
            if (bb_map.get((turn, pt), 0) >> i) & 1:
                p_type = pt
                break
                
        if not p_type: continue

        piece_bb = 1 << i
        own_occupancy = occupancies[turn]
        enemy_occupancy = occupancies[enemy_side]

        pseudo_moves = []
        if p_type == PieceType.Pawn:
            pseudo_moves = utils.get_pawn_moves(turn, piece_bb, combined_occupancy, enemy_occupancy, bitboard_utils)
        elif p_type == PieceType.Knight:
            pseudo_moves = utils.get_knight_moves(piece_bb, own_occupancy, bitboard_utils)
        elif p_type == PieceType.King:
            pseudo_moves = utils.get_king_moves(piece_bb, own_occupancy, bitboard_utils)
        elif p_type in [PieceType.Rook, PieceType.Bishop, PieceType.Queen]:
            pseudo_moves = utils.get_sliding_moves(p_type, piece_bb, combined_occupancy, own_occupancy)

        for m in pseudo_moves:
            to_idx = m[1]
            new_bb = clone_and_apply_move(bb, i, to_idx)
            new_map, _, check_combined = new_bb.generate_maps()
            
            king_bb = new_map.get((turn, PieceType.King), 0)
            king_idx = utils.get_lsb_index(king_bb)
            if king_idx == -1: continue

            in_check = utils.is_square_attacked(king_idx, enemy_side, new_map, check_combined, bitboard_utils)
            if not in_check:
                moves.append(m)

    return moves
