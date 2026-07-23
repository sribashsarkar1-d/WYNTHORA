import math
import random

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0

    def ucb1(self, exploration_weight=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

class MonteCarloTreeSearch:
    """
    Monte Carlo Tree Search (MCTS) for exploring massive decision spaces.
    Used by agents to plan complex sequential moves (like a chess engine).
    """
    def __init__(self, exploration_weight=1.41):
        self.exploration_weight = exploration_weight

    def select(self, node):
        while node.children:
            node = max(node.children, key=lambda c: c.ucb1(self.exploration_weight))
        return node

    def expand(self, node, possible_moves):
        for move in possible_moves:
            # Simplistic state transition for simulation
            new_state = node.state + f"->{move}"
            child = MCTSNode(state=new_state, parent=node)
            node.children.append(child)
        return random.choice(node.children) if node.children else node

    def simulate(self, node):
        # Random rollout simulation (returns 1 for win, 0 for loss)
        return random.choice([0.0, 1.0])

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    def run_search(self, initial_state, possible_moves, iterations=100):
        root = MCTSNode(state=initial_state)
        
        for _ in range(iterations):
            leaf = self.select(root)
            if leaf.visits > 0:
                leaf = self.expand(leaf, possible_moves)
            result = self.simulate(leaf)
            self.backpropagate(leaf, result)
            
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.state
