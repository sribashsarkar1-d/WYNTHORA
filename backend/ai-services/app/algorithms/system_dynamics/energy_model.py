from typing import Dict

class EnergyEngine:
    """
    Models the energy production and consumption matrix of a nation.
    Sources: Oil, Gas, Coal, Solar, Wind, Nuclear
    """
    def __init__(self, gdp: float):
        # Base demand scales with GDP (rough proxy)
        self.base_demand = gdp * 0.05
        
        # Initial production mix (percent of total demand met)
        self.production_capacity = {
            "Oil": self.base_demand * 0.35,
            "Gas": self.base_demand * 0.25,
            "Coal": self.base_demand * 0.20,
            "Solar": self.base_demand * 0.05,
            "Wind": self.base_demand * 0.05,
            "Nuclear": self.base_demand * 0.10
        }
        
        self.current_demand = self.base_demand
        
    def step(self, gdp_growth: float, crisis_impacts: Dict[str, float]) -> Dict[str, float]:
        """
        Advance the energy model by one tick.
        crisis_impacts can contain 'oil_price_spike' or 'infrastructure_damage'
        """
        # Demand changes with GDP growth
        self.current_demand *= (1.0 + gdp_growth)
        
        # Apply crisis impacts to fossil fuels
        if "oil_price_spike" in crisis_impacts:
            # High oil prices reduce oil demand/production capacity temporarily
            self.production_capacity["Oil"] *= (1.0 - crisis_impacts["oil_price_spike"])
            
        if "infrastructure_damage" in crisis_impacts:
            # Broad damage hits grid-dependent sources
            for source in self.production_capacity:
                self.production_capacity[source] *= (1.0 - crisis_impacts["infrastructure_damage"])
                
        # Simulate gradual transition to renewables
        transition_rate = 0.005 # 0.5% shift per tick
        fossil_reduction = (self.production_capacity["Coal"] + self.production_capacity["Oil"]) * transition_rate
        
        self.production_capacity["Coal"] -= fossil_reduction * 0.6
        self.production_capacity["Oil"] -= fossil_reduction * 0.4
        
        self.production_capacity["Solar"] += fossil_reduction * 0.6
        self.production_capacity["Wind"] += fossil_reduction * 0.4
        
        total_production = sum(self.production_capacity.values())
        shortfall = max(0.0, self.current_demand - total_production)
        
        # CO2 emissions calculation
        # Coal is dirtiest, Oil next, Gas cleanest fossil. Renewables/Nuclear ~ 0
        co2_emitted = (
            self.production_capacity["Coal"] * 1.5 +
            self.production_capacity["Oil"] * 1.0 +
            self.production_capacity["Gas"] * 0.5
        )
        
        return {
            "total_demand": self.current_demand,
            "total_production": total_production,
            "shortfall": shortfall,
            "co2_emissions": co2_emitted,
            "mix": self.production_capacity.copy()
        }

if __name__ == "__main__":
    engine = EnergyEngine(gdp=10000)
    res = engine.step(gdp_growth=0.02, crisis_impacts={"oil_price_spike": 0.1})
    print(res)
