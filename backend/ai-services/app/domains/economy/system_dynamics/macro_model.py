import logging
import numpy as np
from enum import Enum, auto
from .rk4 import RK4Integrator
from .cge_model import CGEModel
from .pde import FiniteDifferencePDE
from .stochastic import StochasticIntegrator

logger = logging.getLogger("MacroEnvironment")

class MacroState(Enum):
    UNINITIALIZED = auto()
    EQUILIBRIUM = auto()
    SHOCKED = auto()
    RECOVERING = auto()
    CRASHED = auto()

class MacroEnvironment:
    """
    The main coordinator for System Dynamics and ODEs.
    Holds the state of the Macro-Economy and global climate.
    Controlled by a formal Finite State Machine (FSM).
    """
    def __init__(self):
        self.time = 0.0
        self.dt = 0.1
        self.state = MacroState.UNINITIALIZED
        
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
        
        self.transition_to(MacroState.EQUILIBRIUM)

    def transition_to(self, new_state: MacroState):
        if self.state != new_state:
            logger.info(f"MacroEnvironment FSM Transition: {self.state.name} -> {new_state.name}")
            self.state = new_state

    def evaluate_state_transitions(self):
        """FSM Logic to determine macro state transitions based on market conditions"""
        if self.market_index < 500:
            self.transition_to(MacroState.CRASHED)
        elif self.market_vol > 0.40:
            self.transition_to(MacroState.SHOCKED)
        elif self.state in [MacroState.SHOCKED, MacroState.CRASHED] and self.market_drift > 0:
            self.transition_to(MacroState.RECOVERING)
        elif self.state == MacroState.RECOVERING and self.market_vol < 0.25 and self.market_index > 800:
            self.transition_to(MacroState.EQUILIBRIUM)

    def tick(self):
        """
        Advances the global macro simulation by one time step based on FSM state.
        """
        self.evaluate_state_transitions()
        
        # FSM-specific logic
        if self.state == MacroState.CRASHED:
            self.market_drift = min(self.market_drift, -0.05)
            self.cge_model.F *= 0.95 # Demand destruction
        elif self.state == MacroState.SHOCKED:
            self.market_vol = min(self.market_vol * 1.05, 0.8) # Volatility clustering
            self.cge_model.F *= 0.98
        elif self.state == MacroState.RECOVERING:
            self.market_drift = max(self.market_drift, 0.08) # Rebound growth
            self.cge_model.F *= 1.02
        elif self.state == MacroState.EQUILIBRIUM:
            self.cge_model.F += np.random.normal(0, 1, 3) # Normal fluctuations
            
        self.economy_output = self.cge_model.solve_equilibrium()
        self.co2_pde.step()
        
        # Prevent negative market index
        self.market_index = max(1.0, self.sde.step_gbm(self.market_index, self.market_drift, self.market_vol))
        
        self.time += self.dt

    def get_state(self) -> dict:
        return {
            "time": self.time,
            "fsm_state": self.state.name,
            "agriculture_output": self.economy_output.get('Agriculture Output', 0) if self.economy_output else 0,
            "manufacturing_output": self.economy_output.get('Manufacturing Output', 0) if self.economy_output else 0,
            "services_output": self.economy_output.get('Services Output', 0) if self.economy_output else 0,
            "max_co2_ppm": float(np.max(self.co2_pde.u)),
            "market_index": float(self.market_index)
        }
