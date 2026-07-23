from typing import Dict, Any

class InfrastructureEngine:
    """
    Models the degradation and maintenance of critical national infrastructure.
    Types: Roads, Ports, Railways, Power Grid, Internet
    """
    def __init__(self, initial_quality: float = 1.0):
        # 1.0 = perfect condition, 0.0 = completely destroyed
        self.infrastructure_state = {
            "Roads": initial_quality,
            "Ports": initial_quality,
            "Railways": initial_quality,
            "Power_Grid": initial_quality,
            "Internet": initial_quality
        }
        
        # Inherent degradation per tick
        self.degradation_rates = {
            "Roads": 0.02,
            "Ports": 0.015,
            "Railways": 0.01,
            "Power_Grid": 0.008,
            "Internet": 0.005
        }
        
    def step(self, government_investment: float, crisis_damage: float) -> Dict[str, Any]:
        """
        Advance the infrastructure state.
        `government_investment` comes from tax revenues/subsidies allocated to infra.
        `crisis_damage` comes from extreme events (Hurricane, Flood, War).
        """
        
        investment_per_sector = government_investment / 5.0
        overall_health = 0.0
        
        for sector in self.infrastructure_state:
            # Apply natural degradation and sudden crisis damage
            current = self.infrastructure_state[sector]
            current -= self.degradation_rates[sector]
            current -= crisis_damage
            
            # Apply government upgrades (diminishing returns logic: harder to fix as it gets closer to 1.0)
            upgrade_effect = investment_per_sector * (1.1 - current) 
            current += upgrade_effect
            
            # Clamp between 0.0 and 1.0
            self.infrastructure_state[sector] = max(0.0, min(1.0, current))
            overall_health += self.infrastructure_state[sector]
            
        avg_health = overall_health / 5.0
        
        # Calculate economic penalty from poor infrastructure
        economic_efficiency = 1.0
        if avg_health < 0.8:
            economic_efficiency = 1.0 - ((0.8 - avg_health) * 0.5) # e.g. 0.6 health -> 0.9 efficiency
            
        return {
            "state": self.infrastructure_state.copy(),
            "average_health": avg_health,
            "economic_efficiency": economic_efficiency
        }

if __name__ == "__main__":
    engine = InfrastructureEngine(initial_quality=0.8)
    
    print("Normal year:")
    print(engine.step(government_investment=0.05, crisis_damage=0.0))
    
    print("Hurricane strikes (heavy damage, low investment):")
    print(engine.step(government_investment=0.01, crisis_damage=0.20))
