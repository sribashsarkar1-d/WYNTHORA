import numpy as np
import pandas as pd # type: ignore
from scipy.integrate import odeint # type: ignore
import logging

class SEIRModel:
    """
    Susceptible-Exposed-Infectious-Recovered-Dead (SEIRD) Pandemic Model.
    Includes Hospital Capacity, Vaccination Rollout, and Dynamic Mortality.
    """
    def __init__(self, population: int, initial_infected: int = 1):
        self.logger = logging.getLogger("SEIRD_Model")
        
        # Total population
        self.N = population
        
        # Initial conditions
        self.I0 = initial_infected  # Initial infectious
        self.E0 = 0                 # Initial exposed
        self.R0 = 0                 # Initial recovered (or vaccinated)
        self.D0 = 0                 # Initial dead
        self.S0 = self.N - self.I0 - self.E0 - self.R0 - self.D0
        
        # Epidemiological parameters
        self.beta = 0.15  # Transmission rate (reduced from 0.35 to avoid explosion)
        self.sigma = 0.2  # Incubation rate (1/incubation_period)
        self.gamma = 0.1  # Recovery rate (1/infectious_period)
        self.base_mortality = 0.01 # Base daily mortality rate for infected
        
        # System capacities and interventions
        self.hospital_capacity = self.N * 0.05 # 5% of population can be hospitalized
        self.vaccination_rate = 0.0 # Daily vaccination rate (fraction of susceptible)
        
    def _deriv(self, y, t, N, beta, sigma, gamma, hospital_cap, v_rate, base_mu):
        """
        Differential equations for SEIRD model with vaccination and capacity constraints.
        """
        S, E, I, R, D = y
        
        # Dynamic lockdown: Government enforces restrictions if >1% infected
        if I > N * 0.01:
            beta = beta * 0.5
            
        # Dynamic mortality: spikes if I > hospital_cap
        if I > hospital_cap:
            # Overwhelmed hospitals
            mu = base_mu * 2.5
        else:
            mu = base_mu
            
        dSdt = -beta * S * I / N - (v_rate * S)
        dEdt = beta * S * I / N - sigma * E
        dIdt = sigma * E - gamma * I - mu * I
        dRdt = gamma * I + (v_rate * S)
        dDdt = mu * I
        
        return dSdt, dEdt, dIdt, dRdt, dDdt

    def simulate(self, days: int) -> pd.DataFrame:
        """
        Runs the SEIRD simulation over a given number of days.
        """
        t = np.linspace(0, days, days)
        y0 = self.S0, self.E0, self.I0, self.R0, self.D0
        
        ret = odeint(self._deriv, y0, t, args=(self.N, self.beta, self.sigma, self.gamma, self.hospital_capacity, self.vaccination_rate, self.base_mortality))
        S, E, I, R, D = ret.T
        
        df = pd.DataFrame({
            'Day': range(days),
            'Susceptible': S,
            'Exposed': E,
            'Infectious': I,
            'Recovered': R,
            'Dead': D
        })
        
        self.logger.info(f"Simulated SEIRD model for {days} days.")
        return df
        
    def step(self):
        """Advances the model by 1 day."""
        t = [0, 1]
        y0 = self.S0, self.E0, self.I0, self.R0, self.D0
        ret = odeint(self._deriv, y0, t, args=(self.N, self.beta, self.sigma, self.gamma, self.hospital_capacity, self.vaccination_rate, self.base_mortality))
        S, E, I, R, D = ret[1]
        
        self.S0, self.E0, self.I0, self.R0, self.D0 = S, E, I, R, D
        self.N = S + E + I + R # Update living population
        
    @property
    def I(self):
        return self.I0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Start with a severe pandemic and some vaccination
    model = SEIRModel(population=10_000_000, initial_infected=1000)
    model.vaccination_rate = 0.005 # 0.5% vaccinated per day
    results = model.simulate(days=100)
    print(results.head())
    print(results.tail())
