import numpy as np
from hmmlearn import hmm

class GeopoliticalHMM:
    """
    Hidden Markov Model for Global Geopolitical States.
    States: 
    0: PEACE
    1: TRADE_TENSION
    2: SANCTIONS
    3: CONFLICT
    4: WAR
    5: RECOVERY
    """
    def __init__(self):
        self.states = ["PEACE", "TRADE_TENSION", "SANCTIONS", "CONFLICT", "WAR", "RECOVERY"]
        self.n_states = len(self.states)
        
        # Initialize a Multinomial HMM
        self.model = hmm.CategoricalHMM(n_components=self.n_states, random_state=42)
        
        # Define initial probabilities (Start in PEACE mostly)
        self.model.startprob_ = np.array([0.6, 0.2, 0.05, 0.05, 0.0, 0.1])
        
        # Transition Matrix (Probability of moving from state i to state j)
        self.model.transmat_ = np.array([
            # P,    TT,   S,    C,    W,    R
            [0.70, 0.20, 0.10, 0.00, 0.00, 0.00], # PEACE
            [0.20, 0.50, 0.20, 0.10, 0.00, 0.00], # TRADE_TENSION
            [0.05, 0.15, 0.60, 0.20, 0.00, 0.00], # SANCTIONS
            [0.00, 0.00, 0.10, 0.60, 0.30, 0.00], # CONFLICT
            [0.00, 0.00, 0.00, 0.00, 0.70, 0.30], # WAR
            [0.40, 0.00, 0.00, 0.00, 0.00, 0.60]  # RECOVERY
        ])
        
        # Emission Matrix (Observing indicators: 0=Normal, 1=High Risk, 2=Severe Crisis)
        self.model.emissionprob_ = np.array([
            [0.8, 0.2, 0.0], # PEACE
            [0.5, 0.4, 0.1], # TRADE_TENSION
            [0.3, 0.5, 0.2], # SANCTIONS
            [0.1, 0.5, 0.4], # CONFLICT
            [0.0, 0.1, 0.9], # WAR
            [0.6, 0.3, 0.1]  # RECOVERY
        ])
        
        self.current_state = 0 # Start in PEACE
        
    def step(self, observation):
        """
        Predict the most likely hidden state sequence given observations.
        Observation should be a list of 1D array of integers [0, 1, 2].
        """
        # We can decode the sequence using Viterbi
        obs_seq = np.array([observation]).reshape(-1, 1)
        logprob, state_sequence = self.model.decode(obs_seq, algorithm="viterbi")
        self.current_state = state_sequence[-1]
        return self.states[self.current_state]
        
    def simulate_future(self, n_steps=5):
        """
        Sample future states and observations.
        """
        # To sample from the current state, we need to hack the startprob
        old_start = np.copy(self.model.startprob_)
        new_start = np.zeros(self.n_states)
        new_start[self.current_state] = 1.0
        self.model.startprob_ = new_start
        
        X, Z = self.model.sample(n_samples=n_steps)
        self.model.startprob_ = old_start # restore
        
        return [self.states[z] for z in Z]

if __name__ == "__main__":
    g_hmm = GeopoliticalHMM()
    # Let's say we observe normal conditions for 3 ticks, then severe crisis
    obs = [0, 0, 1, 2, 2]
    print(f"Observations: {obs}")
    
    current_regime = g_hmm.step(obs)
    print(f"Decoded Current State: {current_regime}")
    
    future = g_hmm.simulate_future(n_steps=5)
    print(f"Simulated Next 5 States: {future}")
