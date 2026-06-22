import random
from typing import Dict, Any

class ElectionEngine:
    """
    Simulates national elections, determining if the incumbent government 
    retains power or is replaced based on citizen satisfaction and macro economy.
    """
    def __init__(self):
        self.parties = ["Conservative", "Liberal", "Progressive", "Nationalist"]
        
    def hold_election(self, nation_state: Any) -> Dict[str, Any]:
        """
        Hold an election in a specific NationState.
        Takes into account the nation's GDP health, inflation, and recent crises.
        """
        # Calculate incumbent approval rating
        approval_base = 0.50
        
        # Economic factors
        gdp_health = nation_state.gdp / 1000.0  # Normalized baseline
        if gdp_health > 1.2:
            approval_base += 0.15 # Strong economy boosts approval
        elif gdp_health < 0.8:
            approval_base -= 0.20 # Weak economy hurts approval
            
        # Inflation/interest rate penalty
        if nation_state.interest_rate > 0.10:
            approval_base -= 0.10 # High interest rates hurt
            
        # Random noise (scandals, campaigns)
        approval_base += random.uniform(-0.1, 0.1)
        
        incumbent_wins = approval_base >= 0.50
        
        election_result = {
            "iso_code": nation_state.iso_code,
            "incumbent_wins": incumbent_wins,
            "approval_rating": approval_base
        }
        
        # Policy Change
        if not incumbent_wins:
            new_party = random.choice(self.parties)
            election_result["new_ruling_party"] = new_party
            
            # Apply Policy Changes
            if new_party == "Conservative":
                nation_state.tax_rate = max(0.10, nation_state.tax_rate - 0.05)
                nation_state.subsidies *= 0.5 # Cut subsidies
                nation_state.military_spending_pct += 0.01
            elif new_party == "Liberal":
                nation_state.tax_rate += 0.02
                nation_state.subsidies += nation_state.gdp * 0.02
                nation_state.trade_agreements.append("Free Trade Expansion")
            elif new_party == "Progressive":
                nation_state.tax_rate += 0.10
                nation_state.subsidies += nation_state.gdp * 0.05
                nation_state.military_spending_pct *= 0.8 # Cut defense
            elif new_party == "Nationalist":
                nation_state.tax_rate += 0.05
                nation_state.trade_agreements = [] # Protectionism
                nation_state.military_spending_pct += 0.03
                
            election_result["policy_shift"] = f"Shifted to {new_party} policies"
        else:
            election_result["new_ruling_party"] = "Incumbent"
            election_result["policy_shift"] = "Status Quo maintained"
            
        return election_result
