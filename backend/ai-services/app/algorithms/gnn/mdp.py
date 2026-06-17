import numpy as np

class MarkovDecisionProcess:
    """
    Solves a Markov Decision Process (MDP) using Value Iteration.
    Used by AI national leaders to plan strategic moves.
    """
    def __init__(self, states, actions, transition_probs, rewards, gamma=0.9):
        """
        :param states: List of state names (e.g. ['PEACE', 'WAR'])
        :param actions: List of action names (e.g. ['TRADE', 'ATTACK'])
        :param transition_probs: Dict {state: {action: {next_state: prob}}}
        :param rewards: Dict {state: {action: reward_float}}
        """
        self.states = states
        self.actions = actions
        self.P = transition_probs
        self.R = rewards
        self.gamma = gamma # Discount factor
        self.V = {s: 0.0 for s in states} # State Values
        self.policy = {s: actions[0] for s in states} # Optimal Policy

    def value_iteration(self, max_iter=100, theta=1e-4):
        for _ in range(max_iter):
            delta = 0
            for s in self.states:
                v = self.V[s]
                # Calculate Q-values for all actions
                action_values = {}
                for a in self.actions:
                    q = self.R[s].get(a, 0.0)
                    if s in self.P and a in self.P[s]:
                        for next_s, prob in self.P[s][a].items():
                            q += self.gamma * prob * self.V[next_s]
                    action_values[a] = q
                
                # Update Value and Policy
                best_action = max(action_values, key=action_values.get)
                self.V[s] = action_values[best_action]
                self.policy[s] = best_action
                
                delta = max(delta, abs(v - self.V[s]))
            
            if delta < theta:
                break

    def get_optimal_policy(self):
        return self.policy
