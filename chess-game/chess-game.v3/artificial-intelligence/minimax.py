# 1. Create a GameTree, each node represents a game state
# 2. Evaluation of terminal nodes (final possible states of the game)
#    - win for MAX_player results in +1
#    - win for MIN_player results in -1
#    - draw results in 0
# 3. Backtracking through the game tree
#    - if the current player is MAX, algorithm selects the maximum value (the best possible move) from child nodes to increase the score
#    - if the current player is MIN, algorithm selects the minimum value (a move which minimize MAX advantage) from the child nodes to minimize MAX advantage
#    - Backtracking continues until the algorithm reaches the root node
# 4. Mini-Max operates as depth-first search algorithm
# 5. Once algorithm has propagated values back to the root node, it chooses the move associated with the highest value for MAX (max player)

class GameTreeNode:
    def __init__(self, value=None, children=None):
        if children is None:
            children = []
        self.value = value  # Leaf node's value or None for intermediate nodes
        self.children = children  # List of child nodes

def minimax(node: GameTreeNode, depth: int, is_maximizing_player: bool):
    if depth == 0 or not node.children:
        return node.value

    if is_maximizing_player:
        max_eval = float('-inf')
        for child in node.children:
            val = minimax(child, depth - 1, False)
            max_eval = max(max_eval, val)

        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children:
            val = minimax(child, depth - 1, True)
            min_eval = min(min_eval, val)

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

result = minimax(root, 3, True)
print(f"Optimal value using MinMax: {result}")