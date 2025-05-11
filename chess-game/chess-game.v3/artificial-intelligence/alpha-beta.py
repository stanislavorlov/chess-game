# optimization technique of Mini-Max algorithm
# reduces the number of nodes by cutting off branches that won't affect final decision

# two values are used on each step of the algorithm:
# - alpha: represents the best value the maximizing player can guarantee so far
# - beta: represents the best value the minimizing player can guarantee so far

# if algorithm finds that a particular branch can't improve the final outcome, it prunes it

# alpha: the best score that maximizing player can guarantee at a given level or above.
# Maximizing player looking for highest possible score.

# beta: the best score that minimizing player can guarantee at a given level ot below.
# Minimizing player looking for lowest possible score.

class GameTreeNode:
    def __init__(self, value=None, children=None):
        self.value = value  # Leaf node's value or None for intermediate nodes
        self.children = children if children else []  # List of child nodes

def alpha_beta_pruning(node, depth, alpha, beta, maximizing_player):
    # Base case: if we reach a leaf node or the maximum depth
    if depth == 0 or not node.children:
        return node.value  # Return the heuristic value of the node

    if maximizing_player:
        max_eval = float('-inf')
        for child in node.children:
            eval_value = alpha_beta_pruning(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            eval_value = alpha_beta_pruning(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

# Leaf nodes with values (the evaluation scores of game outcomes)
leaf1 = GameTreeNode(3)
leaf2 = GameTreeNode(5)
leaf3 = GameTreeNode(2)
leaf4 = GameTreeNode(9)
leaf5 = GameTreeNode(0)
leaf6 = GameTreeNode(-1)
leaf7 = GameTreeNode(7)
leaf8 = GameTreeNode(4)

# Intermediate nodes with children
nodeB = GameTreeNode(None, [leaf1, leaf2])
nodeC = GameTreeNode(None, [leaf3, leaf4])
nodeD = GameTreeNode(None, [leaf5, leaf6])
nodeE = GameTreeNode(None, [leaf7, leaf8])

root = GameTreeNode(None, [nodeB, nodeC, nodeD, nodeE])

result = alpha_beta_pruning(root, 3, float('-inf'), float('inf'), True)
print(f"Optimal value using Alpha-Beta Pruning: {result}")