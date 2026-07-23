import numpy as np

class HiddenMarkovModel:
    """
    Hidden Markov Model using the Viterbi Algorithm.
    Used to infer hidden states (e.g., secretly preparing for war) from observable actions.
    """
    def __init__(self, states, observations, start_prob, trans_prob, emit_prob):
        self.states = states
        self.obs = observations
        self.start_p = start_prob # Initial state probabilities
        self.trans_p = trans_prob # Transition matrix
        self.emit_p = emit_prob   # Emission (Observation) matrix

    def viterbi(self, obs_sequence):
        """
        Calculates the most likely sequence of hidden states given an observation sequence.
        """
        V = [{}]
        path = {}

        # Initialize base cases (t == 0)
        for y in self.states:
            V[0][y] = self.start_p[y] * self.emit_p[y].get(obs_sequence[0], 0)
            path[y] = [y]

        # Run Viterbi for t > 0
        for t in range(1, len(obs_sequence)):
            V.append({})
            newpath = {}

            for y in self.states:
                # Find the max probability state transition to this state y
                (prob, state) = max(
                    (V[t-1][y0] * self.trans_p[y0].get(y, 0) * self.emit_p[y].get(obs_sequence[t], 0), y0)
                    for y0 in self.states
                )
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            path = newpath

        # Find the final most probable state and path
        n = len(obs_sequence) - 1
        (prob, state) = max((V[n][y], y) for y in self.states)
        return prob, path[state]
