import math
import random

class UCBBandit:
    """
    Upper Confidence Bound (UCB1) algorithm for Multi-Armed Bandit problems.
    Used by agents to explore different job sectors or investments.
    """
    def __init__(self, arms, exploration_weight=1.0):
        self.arms = arms
        self.counts = {arm: 0 for arm in arms}
        self.values = {arm: 0.0 for arm in arms}
        self.total_pulls = 0
        self.c = exploration_weight

    def select_arm(self):
        # Play each arm at least once to initialize
        for arm in self.arms:
            if self.counts[arm] == 0:
                return arm

        best_score = -float('inf')
        best_arm = None

        for arm in self.arms:
            exploitation = self.values[arm]
            exploration = self.c * math.sqrt(math.log(self.total_pulls) / self.counts[arm])
            score = exploitation + exploration
            
            if score > best_score:
                best_score = score
                best_arm = arm
                
        return best_arm

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.total_pulls += 1
        
        n = self.counts[arm]
        value = self.values[arm]
        
        # Running average formula
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[arm] = new_value

class EpsilonGreedyBandit:
    def __init__(self, arms, epsilon=0.1):
        self.arms = arms
        self.counts = {arm: 0 for arm in arms}
        self.values = {arm: 0.0 for arm in arms}
        self.epsilon = epsilon

    def select_arm(self):
        if random.random() < self.epsilon:
            return random.choice(self.arms)
        
        # Exploit: return arm with max value
        return max(self.values.items(), key=lambda x: x[1])[0]

    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        self.values[arm] = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
