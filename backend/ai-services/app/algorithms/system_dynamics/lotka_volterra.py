import numpy as np

class LotkaVolterraEconomy:
    """
    Adapts the Lotka-Volterra (Predator-Prey) equations to Macro-Economics.
    x = Prey (e.g., Labor/Workers)
    y = Predator (e.g., Automation/Capital)
    
    dx/dt = alpha*x - beta*x*y
    dy/dt = delta*x*y - gamma*y
    """
    def __init__(self, alpha=0.1, beta=0.02, delta=0.01, gamma=0.1):
        self.alpha = alpha  # Labor growth rate
        self.beta = beta    # Rate at which automation displaces labor
        self.delta = delta  # Rate at which capital grows from exploiting labor
        self.gamma = gamma  # Capital depreciation rate without labor

    def derivative(self, t, state):
        """
        Returns [dx/dt, dy/dt]
        state = [x, y]
        """
        x, y = state[0], state[1]
        dx_dt = self.alpha * x - self.beta * x * y
        dy_dt = self.delta * x * y - self.gamma * y
        return np.array([dx_dt, dy_dt])
