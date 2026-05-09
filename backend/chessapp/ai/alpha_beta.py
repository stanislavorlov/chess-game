from typing import Tuple, Optional
from .bitboards import Bitboards, Side
from .bitboard_utils import BitboardUtils
from .game_state import get_legal_moves, clone_and_apply_move
from .evaluation import evaluate_board

def alpha_beta(
    bb: Bitboards, 
    depth: int, 
    alpha: float, 
    beta: float, 
    is_maximizing: bool, 
    turn: Side, 
    utils: BitboardUtils
) -> float:
    if depth == 0:
        return evaluate_board(bb)

    legal_moves = get_legal_moves(bb, turn, utils)
    if not legal_moves:
        return -10000.0 if is_maximizing else 10000.0

    if is_maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            next_bb = clone_and_apply_move(bb, move[0], move[1])
            eval_val = alpha_beta(next_bb, depth - 1, alpha, beta, False, Side.Black if turn == Side.White else Side.White, utils)
            max_eval = max(max_eval, eval_val)
            alpha = max(alpha, eval_val)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            next_bb = clone_and_apply_move(bb, move[0], move[1])
            eval_val = alpha_beta(next_bb, depth - 1, alpha, beta, True, Side.Black if turn == Side.White else Side.White, utils)
            min_eval = min(min_eval, eval_val)
            beta = min(beta, eval_val)
            if beta <= alpha: break
        return min_eval

def get_best_move(bb: Bitboards, depth: int, turn: Side) -> Optional[Tuple[int, int]]:
    utils = BitboardUtils()
    best_move = None
    
    legal_moves = get_legal_moves(bb, turn, utils)
    if not legal_moves: return None

    is_maximizing = (turn == Side.White)
    alpha = -float('inf')
    beta = float('inf')

    if is_maximizing:
        best_val = -float('inf')
        for move in legal_moves:
            next_bb = clone_and_apply_move(bb, move[0], move[1])
            move_val = alpha_beta(next_bb, depth - 1, alpha, beta, False, Side.Black, utils)
            if move_val > best_val:
                best_val = move_val
                best_move = move
            alpha = max(alpha, best_val)
    else:
        best_val = float('inf')
        for move in legal_moves:
            next_bb = clone_and_apply_move(bb, move[0], move[1])
            move_val = alpha_beta(next_bb, depth - 1, alpha, beta, True, Side.White, utils)
            if move_val < best_val:
                best_val = move_val
                best_move = move
            beta = min(beta, best_val)

    return best_move
