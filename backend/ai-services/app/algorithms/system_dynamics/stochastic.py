import numpy as np

class StochasticIntegrator:
    """
    Euler-Maruyama method for integrating Stochastic Differential Equations (SDEs).
    Primarily uses Geometric Brownian Motion (GBM): dS = mu*S*dt + sigma*S*dW
    Essential for simulating highly volatile financial markets or crypto fluctuations.
    """
    def __init__(self, dt=0.1):
        self.dt = dt

    def step_gbm(self, S, mu, sigma):
        """
        Takes one step of Geometric Brownian Motion.
        :param S: Current price/value.
        :param mu: Expected return (drift).
        :param sigma: Volatility (standard deviation).
        :return: New price S_{t+dt}
        """
        # Generate Weiner process increment dW (Normal distribution N(0, sqrt(dt)))
        dW = np.random.normal(0, np.sqrt(self.dt))
        
        # S_{t+dt} = S_t + mu * S_t * dt + sigma * S_t * dW
        dS = mu * S * self.dt + sigma * S * dW
        return max(S + dS, 0.0) # Price cannot drop below 0
