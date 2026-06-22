import numpy as np
import random
from typing import Dict, Tuple

class PolicyRLAgent:
    """
    Reinforcement Learning Agent (Q-Learning proxy for PPO) designed to
    optimize government policy (Tax Rates, Interest Rates) to maximize GDP
    and minimize inflation.
    """
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.95, epsilon: float = 0.1):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        # State space: (GDP Health, Inflation Level)
        # GDP: 0 (Low), 1 (Normal), 2 (High)
        # Inflation: 0 (Low), 1 (Normal), 2 (High)
        
        # Action space: (Tax Change, Rate Change)
        # 0: (-0.01, 0), 1: (+0.01, 0), 2: (0, -0.01), 3: (0, +0.01), 4: (0, 0)
        self.q_table = np.zeros((3, 3, 5))
        
        self.actions = [
            {"tax": -0.01, "rate": 0.0},
            {"tax": 0.01, "rate": 0.0},
            {"tax": 0.0, "rate": -0.01},
            {"tax": 0.0, "rate": 0.01},
            {"tax": 0.0, "rate": 0.0}
        ]

    def _discretize_state(self, gdp_growth: float, inflation: float) -> Tuple[int, int]:
        gdp_state = 1
        if gdp_growth < 0.0: gdp_state = 0
        elif gdp_growth > 0.03: gdp_state = 2
        
        inf_state = 1
        if inflation < 0.01: inf_state = 0
        elif inflation > 0.05: inf_state = 2
        
        return (gdp_state, inf_state)

    def choose_action(self, gdp_growth: float, inflation: float) -> Tuple[Dict[str, float], int, Tuple[int, int]]:
        """
        Epsilon-greedy action selection.
        """
        state = self._discretize_state(gdp_growth, inflation)
        
        if random.uniform(0, 1) < self.epsilon:
            action_idx = random.randint(0, 4)
        else:
            action_idx = int(np.argmax(self.q_table[state[0], state[1]]))
            
        return self.actions[action_idx], action_idx, state

    def learn(self, old_state: Tuple[int, int], action_idx: int, reward: float, new_gdp: float, new_inf: float):
        """
        Q-learning update.
        """
        new_state = self._discretize_state(new_gdp, new_inf)
        
        old_q = self.q_table[old_state[0], old_state[1], action_idx]
        max_future_q = np.max(self.q_table[new_state[0], new_state[1]])
        
        new_q = old_q + self.lr * (reward + self.gamma * max_future_q - old_q)
        self.q_table[old_state[0], old_state[1], action_idx] = new_q

    def calculate_reward(self, gdp_growth: float, inflation: float) -> float:
        """
        Reward function: maximize growth, heavily penalize high inflation.
        """
        reward = gdp_growth * 100.0
        if inflation > 0.05:
            reward -= (inflation - 0.05) * 200.0
        return reward

if __name__ == "__main__":
    # Test training loop
    agent = PolicyRLAgent()
    epochs = 100
    steps_per_epoch = 20
    
    for epoch in range(epochs):
        gdp, inf = 0.02, 0.02 # Reset environment
        total_reward = 0
        
        for step in range(steps_per_epoch):
            action, idx, state = agent.choose_action(gdp, inf)
            
            # Simulate environment reaction
            new_gdp = gdp - action["tax"] * 0.5 - action["rate"] * 0.2
            new_inf = inf + action["tax"] * 0.1 - action["rate"] * 0.5
            
            # Add noise
            new_gdp += random.normalvariate(0, 0.005)
            new_inf += random.normalvariate(0, 0.002)
            
            reward = agent.calculate_reward(new_gdp, new_inf)
            agent.learn(state, idx, reward, new_gdp, new_inf)
            
            gdp, inf = new_gdp, new_inf
            total_reward += reward
            
        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{epochs} | Total Reward: {total_reward:.2f}")
            
    print("\nTraining complete. Q-Table Insights:")
    active_q = agent.q_table[agent.q_table != 0]
    if len(active_q) > 0:
        print(f"Max Q-Value discovered: {np.max(agent.q_table):.2f}")
        print(f"Mean Q-Value of explored states: {np.mean(active_q):.2f}")
    else:
        print("Agent failed to learn any positive rewards.")
