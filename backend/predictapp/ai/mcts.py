import math
import numpy as np
from typing import List, Optional, Tuple, Dict
from .bitboards import Bitboards, Side
from .bitboard_utils import BitboardUtils
from .game_state import get_legal_moves, clone_and_apply_move
from .keras_model import ChessZeroModel

class MCTSNode:
    def __init__(self, bb: Bitboards, turn: Side, parent=None, move=None, prior_prob=0.0):
        self.bb = bb
        self.turn = turn
        self.parent = parent
        self.move = move # The move (from_sq, to_sq) that led to this node
        self.prior_prob = prior_prob
        
        self.children: Dict[Tuple[int, int], 'MCTSNode'] = {}
        self.visit_count = 0
        self.value_sum = 0.0
        self.is_expanded = False

    @property
    def q_value(self) -> float:
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

class MonteCarloTreeSearch:
    def __init__(self, model: ChessZeroModel, c_puct: float = 1.0):
        self.model = model
        self.c_puct = c_puct
        self.utils = BitboardUtils()

    def search(self, initial_bb: Bitboards, turn: Side, num_simulations: int = 100) -> Optional[Tuple[int, int]]:
        root = MCTSNode(initial_bb, turn)

        for _ in range(num_simulations):
            node = root
            
            # 1. Selection
            while node.is_expanded and len(node.children) > 0:
                node = self._select_child(node)

            # 2. Expansion and Evaluation
            if not node.is_expanded:
                value = self._expand_and_evaluate(node)
                # 3. Backpropagation
                self._backpropagate(node, value)
            else:
                # Terminal state reached in selection
                legal_moves = get_legal_moves(node.bb, node.turn, self.utils)
                if not legal_moves:
                    self._backpropagate(node, -1.0)
                else:
                    self._backpropagate(node, 0.0)

        best_move = None
        best_visits = -1
        
        for move, child in root.children.items():
            if child.visit_count > best_visits:
                best_visits = child.visit_count
                best_move = move
                
        return best_move

    def _select_child(self, node: MCTSNode) -> MCTSNode:
        best_score = -float('inf')
        best_child = None
        
        # PUCT formula
        for child in node.children.values():
            u = self.c_puct * child.prior_prob * math.sqrt(node.visit_count) / (1 + child.visit_count)
            # We negate child's Q because it's the value for the opponent
            score = -child.q_value + u
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child

    def _expand_and_evaluate(self, node: MCTSNode) -> float:
        legal_moves = get_legal_moves(node.bb, node.turn, self.utils)
        
        if not legal_moves:
            # Terminal state
            node.is_expanded = True
            return -1.0 # Loss for the player whose turn it is

        policy, value = self.model.predict(node.bb)
        
        # Create children and assign prior probabilities
        policy_sum = 0.0
        for move in legal_moves:
            from_sq, to_sq = move
            policy_idx = from_sq * 64 + to_sq
            # Extract prior probability
            prob = float(policy[policy_idx])
            
            next_bb = clone_and_apply_move(node.bb, from_sq, to_sq)
            next_turn = Side.Black if node.turn == Side.White else Side.White
            
            child = MCTSNode(next_bb, next_turn, parent=node, move=move, prior_prob=prob)
            node.children[move] = child
            policy_sum += prob
            
        # Normalize probabilities over legal moves
        if policy_sum > 0:
            for child in node.children.values():
                child.prior_prob /= policy_sum
        else:
            # Fallback if network outputs 0 for all legal moves
            prob = 1.0 / len(legal_moves)
            for child in node.children.values():
                child.prior_prob = prob
                
        node.is_expanded = True
        return float(value)

    def _backpropagate(self, node: MCTSNode, value: float):
        current = node
        v = value
        
        while current is not None:
            current.visit_count += 1
            current.value_sum += v
            v = -v # Opponent's perspective
            current = current.parent
