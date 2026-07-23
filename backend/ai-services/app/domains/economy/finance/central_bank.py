class CentralBank:
    """
    Simulates a unified global/national Central Bank applying the Taylor Rule,
    Quantitative Easing (QE), and Money Supply mechanics.
    """
    def __init__(self, target_inflation: float = 0.02):
        self.target_inflation = target_inflation
        self.interest_rate = 0.05
        self.money_supply = 20000.0 # Billion
        self.qe_active = False
        
    def step(self, current_inflation: float, gdp_growth: float) -> dict:
        # Taylor Rule proxy
        inflation_gap = current_inflation - self.target_inflation
        growth_gap = gdp_growth - 0.03 # assume 3% is full employment growth proxy
        
        # Adjust interest rates
        rate_change = 0.5 * inflation_gap + 0.5 * growth_gap
        self.interest_rate = max(0.0, min(0.20, self.interest_rate + rate_change * 0.1))
        
        # QE Logic (if growth is very negative and rate is near 0)
        if gdp_growth < -0.02 and self.interest_rate < 0.01:
            self.qe_active = True
            self.money_supply *= 1.05 # Print money
        elif current_inflation > 0.05:
            self.qe_active = False
            self.money_supply *= 0.98 # Quantitative Tightening
            
        return {
            "interest_rate": self.interest_rate,
            "qe_active": self.qe_active,
            "money_supply_b": self.money_supply,
            "inflation_target": self.target_inflation
        }
