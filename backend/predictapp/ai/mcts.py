import math
import time
import random
import numpy as np
from typing import List, Optional, Tuple, Dict
from .bitboards import Bitboards, Side
from .bitboard_utils import BitboardUtils
from .game_state import get_legal_moves, clone_and_apply_move, is_in_check
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

    def search(self, initial_bb: Bitboards, turn: Side, time_limit: float = 1.0, temperature: float = 1.0) -> Optional[Tuple[int, int]]:
        root = MCTSNode(initial_bb, turn)
        
        # Expand root immediately to apply Dirichlet noise
        self._expand_and_evaluate(root)
        self._add_dirichlet_noise(root)

        end_time = time.time() + time_limit
        simulations = 0
        while time.time() < end_time:
            simulations += 1
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
                    if is_in_check(node.bb, node.turn, self.utils):
                        self._backpropagate(node, -1.0) # Loss
                    else:
                        self._backpropagate(node, 0.0) # Stalemate
                else:
                    self._backpropagate(node, 0.0)

        if not root.children:
            return None
            
        moves = list(root.children.keys())
        visits = [child.visit_count for child in root.children.values()]
        
        if temperature < 1e-3:
            # Deterministic selection for temperature -> 0
            best_idx = np.argmax(visits)
            return moves[best_idx]
            
        # Temperature-based probability distribution
        visits_pow = np.power(visits, 1.0 / temperature)
        probs = visits_pow / np.sum(visits_pow)
        
        # Select move based on probabilities
        chosen_idx = np.random.choice(len(moves), p=probs)
        return moves[chosen_idx]

    def _add_dirichlet_noise(self, node: MCTSNode, dirichlet_alpha: float = 0.3, exploration_fraction: float = 0.25):
        if not node.children:
            return
            
        num_children = len(node.children)
        noise = np.random.dirichlet([dirichlet_alpha] * num_children)
        
        for i, child in enumerate(node.children.values()):
            child.prior_prob = (1 - exploration_fraction) * child.prior_prob + exploration_fraction * noise[i]

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
            if is_in_check(node.bb, node.turn, self.utils):
                return -1.0 # Loss for the player whose turn it is
            return 0.0 # Stalemate/Draw

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
