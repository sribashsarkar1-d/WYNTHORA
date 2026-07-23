import numpy as np

class GeometricBrownianMotion:
    """
    Simulates stock price paths using Stochastic Differential Equations (SDE).
    Formula: dS = mu*S*dt + sigma*S*dW
    """
    def __init__(self, mu=0.08, sigma=0.2, dt=1/252):
        self.mu = mu       # Expected return (drift)
        self.sigma = sigma # Volatility
        self.dt = dt       # Time step (default 1 trading day = 1/252 years)

    def simulate_path(self, S0, days=252):
        """
        Generates a sequence of stock prices over a given number of days.
        """
        prices = np.zeros(days)
        prices[0] = S0
        
        for t in range(1, days):
            # dW is the Brownian motion increment
            dW = np.random.normal(0, np.sqrt(self.dt))
            
            # S_{t+1} = S_t * exp((mu - sigma^2/2)*dt + sigma*dW)
            # This is the exact solution to the GBM SDE
            drift = (self.mu - 0.5 * self.sigma**2) * self.dt
            shock = self.sigma * dW
            prices[t] = prices[t-1] * np.exp(drift + shock)
            
        return prices
