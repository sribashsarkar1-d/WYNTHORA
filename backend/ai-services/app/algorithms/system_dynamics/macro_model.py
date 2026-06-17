import numpy as np
from rk4 import RK4Integrator
from lotka_volterra import LotkaVolterraEconomy
from pde import FiniteDifferencePDE
from stochastic import StochasticIntegrator

class MacroEnvironment:
    """
    The main coordinator for System Dynamics and ODEs.
    Holds the state of the Macro-Economy and global climate.
    """
    def __init__(self):
        self.time = 0.0
        self.dt = 0.1
        
        # 1. Labor vs Automation (Lotka-Volterra via RK4)
        self.lv_model = LotkaVolterraEconomy(alpha=0.1, beta=0.02, delta=0.01, gamma=0.1)
        self.rk4 = RK4Integrator(step_size=self.dt)
        self.economy_state = np.array([40.0, 9.0]) # [Laborers, Capital/Automation]
        
        # 2. Global CO2 Diffusion (PDE)
        self.co2_pde = FiniteDifferencePDE(nx=20, length=100.0, alpha=2.0, dt=self.dt)
        self.co2_pde.set_initial_condition(10, 100.0) # Massive factory pollution at center
        
        # 3. Stock Market Index (Stochastic GBM)
        self.sde = StochasticIntegrator(dt=self.dt)
        self.market_index = 1000.0 # Starting index value (e.g., S&P 500 equivalent)
        self.market_drift = 0.05   # 5% expected growth
        self.market_vol = 0.20     # 20% volatility

    def tick(self):
        """
        Advances the global macro simulation by one time step.
        """
        # 1. Update Labor/Automation using RK4
        self.economy_state = self.rk4.step(self.lv_model.derivative, self.time, self.economy_state)
        
        # 2. Diffuse CO2
        self.co2_pde.step()
        
        # 3. Fluctuate Market
        self.market_index = self.sde.step_gbm(self.market_index, self.market_drift, self.market_vol)
        
        self.time += self.dt

    def get_state(self):
        return {
            "Time": round(self.time, 2),
            "Labor Force": round(self.economy_state[0], 2),
            "Capital/Automation": round(self.economy_state[1], 2),
            "Max Local CO2": round(np.max(self.co2_pde.u), 2),
            "Market Index": round(self.market_index, 2)
        }
