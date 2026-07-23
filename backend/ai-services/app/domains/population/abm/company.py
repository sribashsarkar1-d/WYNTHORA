import random
from typing import Dict, Any

class CompanyAgent:
    """
    Simulates a major multinational corporation (e.g., Tesla, Apple, Microsoft).
    Tracks Revenue, Expansion, and Market Share.
    """
    def __init__(self, name: str, sector: str, initial_revenue: float, market_share: float):
        self.name = name
        self.sector = sector
        self.revenue = initial_revenue
        self.market_share = market_share # Percentage (0.0 to 1.0)
        
        # State variables
        self.cash_reserves = initial_revenue * 0.2
        self.r_and_d_spending = 0.05
        self.expansion_aggressiveness = random.uniform(0.1, 0.3)
        self.bankrupt = False
        
    def step(self, sector_growth: float, tax_rate: float, crisis_modifier: float) -> Dict[str, Any]:
        """
        Advance the company by one simulation tick.
        """
        if self.bankrupt:
            return {"name": self.name, "status": "Bankrupt"}
            
        # 1. Calculate Revenue (affected by sector growth and market share)
        base_revenue = self.revenue
        
        # Market shocks
        revenue_shock = random.normalvariate(0, 0.05)
        growth_factor = 1.0 + sector_growth + revenue_shock - crisis_modifier
        
        # Apply R&D bonus
        growth_factor += self.r_and_d_spending
        
        self.revenue = base_revenue * growth_factor
        
        # 2. Expenses and Taxes
        operating_costs = self.revenue * 0.7 # 70% margins approx
        gross_profit = self.revenue - operating_costs
        
        taxes_paid = max(0, gross_profit * tax_rate)
        net_profit = gross_profit - taxes_paid
        
        self.cash_reserves += net_profit
        
        # 3. Reinvestment / Expansion
        if self.cash_reserves > self.revenue * 0.5:
            # Expand market share aggressively
            expansion_cost = self.cash_reserves * self.expansion_aggressiveness
            self.cash_reserves -= expansion_cost
            
            # Gaining market share is hard
            market_share_gain = (expansion_cost / self.revenue) * 0.01 
            self.market_share = min(1.0, self.market_share + market_share_gain)
            
        # 4. Bankruptcy check
        if self.cash_reserves < 0:
            self.bankrupt = True
            self.market_share = 0.0
            self.revenue = 0.0
            
        return {
            "name": self.name,
            "sector": self.sector,
            "revenue": self.revenue,
            "market_share": self.market_share,
            "net_profit": net_profit,
            "cash_reserves": self.cash_reserves,
            "status": "Active"
        }

class CorporateEngine:
    def __init__(self):
        self.companies = [
            CompanyAgent("Apple", "Technology", 380e9, 0.25),
            CompanyAgent("Microsoft", "Technology", 210e9, 0.30),
            CompanyAgent("Amazon", "Services", 500e9, 0.40),
            CompanyAgent("Google", "Technology", 280e9, 0.45),
            CompanyAgent("Lockheed Martin", "Defense", 65e9, 0.50),
            CompanyAgent("ExxonMobil", "Energy", 413e9, 0.35),
            CompanyAgent("Walmart", "Retail", 611e9, 0.60),
            CompanyAgent("Toyota", "Automotive", 275e9, 0.40)
        ]
        
    def step(self, global_state: Dict[str, Any]) -> list:
        results = []
        avg_tax = global_state.get("average_tax_rate", 0.20)
        
        tension = global_state.get("geopolitical_tension_modifier", 0.0)
        oil_spike = global_state.get("oil_price_spike", 0.0)
        trade_disruption = global_state.get("trade_disruption", 0.0)
        mfg_shock = global_state.get("manufacturing_output_modifier", 0.0)
        
        for comp in self.companies:
            # Baseline sector growth
            sector_growth = 0.02
            comp_crisis = 0.0
            
            if comp.sector == "Technology":
                sector_growth = 0.05
                comp_crisis = trade_disruption * 0.1
            elif comp.sector == "Defense":
                sector_growth = 0.02 + tension * 0.5
                comp_crisis = -tension * 0.5 # Defense grows during crisis!
            elif comp.sector == "Energy":
                sector_growth = 0.03 + oil_spike * 0.5
                comp_crisis = -oil_spike * 0.2
            elif comp.sector == "Retail":
                sector_growth = 0.03
                comp_crisis = trade_disruption * 0.5
            elif comp.sector == "Automotive":
                sector_growth = 0.02
                comp_crisis = (mfg_shock * -0.5) + trade_disruption * 0.3
            elif comp.sector == "Services":
                sector_growth = 0.04
                comp_crisis = trade_disruption * 0.2
            
            res = comp.step(sector_growth, avg_tax, comp_crisis)
            results.append(res)
            
        return results

if __name__ == "__main__":
    ce = CorporateEngine()
    print("Year 1:", ce.step({"average_tax_rate": 0.20}))
