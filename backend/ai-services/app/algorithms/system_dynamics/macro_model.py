import numpy as np
from rk4 import RK4Integrator
from cge_model import CGEModel
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
        
        # 1. Multi-Sector Input-Output (CGE Model)
        self.cge_model = CGEModel(num_sectors=3)
        self.economy_output = self.cge_model.solve_equilibrium()
        
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
        # 1. Update Economy using CGE
        # For dynamic changes, we might update Final Demand F
        self.cge_model.F += np.random.normal(0, 1, 3) 
        self.economy_output = self.cge_model.solve_equilibrium()
        
        # 2. Diffuse CO2
        self.co2_pde.step()
        
        # 3. Fluctuate Market
        self.market_index = self.sde.step_gbm(self.market_index, self.market_drift, self.market_vol)
        
        self.time += self.dt

    def get_state(self) -> dict:
        return {
            "time": self.time,
            "agriculture_output": self.economy_output.get('Agriculture Output', 0) if self.economy_output else 0,
            "manufacturing_output": self.economy_output.get('Manufacturing Output', 0) if self.economy_output else 0,
            "services_output": self.economy_output.get('Services Output', 0) if self.economy_output else 0,
            "max_co2_ppm": float(np.max(self.co2_pde.u)),
            "market_index": float(self.market_index)
        }
