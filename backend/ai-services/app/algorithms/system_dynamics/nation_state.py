import numpy as np

# Import the existing models
from cge_model import CGEModel # type: ignore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'health')))
from seir_model import SEIRModel # type: ignore

class NationState:
    """
    Represents an individual country in the Digital Twin Earth.
    """
    def __init__(self, iso_code: str, name: str, base_gdp: float, population: int):
        self.iso_code = iso_code
        self.name = name
        self.population = population
        
        # State variables
        self.gdp = base_gdp
        self.tax_rate = 0.20
        self.co2_emissions = base_gdp * 0.5 # Proxy for emissions
        
        # Dynamic Government Policies
        self.interest_rate = 0.05
        self.subsidies = 0.0
        self.sanctions = []
        self.trade_agreements = []
        self.military_spending_pct = 0.02
        
        # Population Dynamics
        self.urbanization_rate = 0.50
        self.birth_rate = 0.015
        self.death_rate = 0.008
        self.net_migration = 0.0
        
        # Sub-models localized to this country
        self.economy = CGEModel(num_sectors=3)
        self.health = SEIRModel(population=population)
        
        # Initialize final demand based on base GDP approximation
        self.economy.F = np.array([base_gdp * 0.1, base_gdp * 0.3, base_gdp * 0.6])
        
    def tick(self, global_co2: float):
        """
        Advances the state of the nation by one tick.
        """
        # 1. Economic Step
        economic_output = self.economy.solve_equilibrium()
        if economic_output:
            self.gdp = sum(economic_output.values())
        
        # 2. Health Step
        # Higher global CO2 slightly increases infection rate due to environmental stress
        # global_co2 is approx 160,000. We scale it reasonably so stress is 1.0 to 1.5 max.
        env_stress = 1.0 + (global_co2 / 1000000.0)
        self.health.beta *= env_stress
        self.health.step()
        self.health.beta /= env_stress # Reset
        
        # 3. Emissions Step
        self.co2_emissions = self.gdp * 0.5
        
        # 4. Population Step
        # Synchronize with pandemic model surviving population
        if hasattr(self.health, 'N'):
            self.population = int(self.health.N)
            
        natural_increase = self.population * (self.birth_rate - self.death_rate)
        
        # Calculate dynamic migration based on GDP per capita proxy
        gdp_per_capita = self.gdp / max(1, self.population)
        if gdp_per_capita > 0.0005: 
            self.net_migration = 0.005 # Net influx
        elif gdp_per_capita < 0.0001:
            self.net_migration = -0.005 # Outflow
        else:
            self.net_migration = 0.0
            
        migration_change = self.population * self.net_migration
        self.population += int(natural_increase + migration_change)
        
        # Sync back to health model
        if hasattr(self.health, 'N'):
            self.health.N = self.population
            
        # Urbanization grows with economic development
        gdp_per_capita = self.gdp / max(1, self.population)
        if gdp_per_capita > 0.00005: 
            self.urbanization_rate = min(0.95, self.urbanization_rate + 0.001)
        
    def get_state(self):
        return {
            "iso_code": self.iso_code,
            "name": self.name,
            "gdp": self.gdp,
            "population": self.population,
            "co2_emissions": self.co2_emissions,
            "infected": self.health.I,
            "tax_rate": self.tax_rate,
            "interest_rate": self.interest_rate,
            "subsidies": self.subsidies,
            "military_spending_pct": self.military_spending_pct,
            "urbanization_rate": self.urbanization_rate
        }
