import numpy as np

class MonteCarloEngine:
    """
    Vectorized Monte Carlo Scenario Engine running 10,000 simulations
    to determine Best Case, Expected Case, and Worst Case macroeconomic futures.
    """
    def __init__(self, num_simulations=10000, days=30):
        self.num_simulations = num_simulations
        self.days = days
        
    def run_scenarios(self, base_gdp: float, base_volatility: float, active_shocks: float):
        """
        Runs Geometric Brownian Motion across 10k parallel universes in numpy.
        """
        dt = 1/252.0
        # Bound the expected growth to prevent unrecoverable simulation collapses
        mu = max(-0.50, 0.03 - active_shocks) 
        # Cap volatility
        sigma = min(0.80, base_volatility + (active_shocks * 0.5))
        
        # Generate random walk for 10000 paths
        Z = np.random.normal(0, 1, (self.num_simulations, self.days))
        
        # Calculate daily returns
        daily_returns = np.exp((mu - 0.5 * sigma**2)*dt + sigma * np.sqrt(dt) * Z)
        
        # Cumulative product over the days
        price_paths = base_gdp * np.cumprod(daily_returns, axis=1)
        
        # Final day values for all 10000 simulations
        final_values = price_paths[:, -1]
        
        best_case = np.percentile(final_values, 95)
        expected_case = np.median(final_values)
        worst_case = np.percentile(final_values, 5)
        
        return {
            "num_simulations": self.num_simulations,
            "days_forecasted": self.days,
            "best_case_gdp": best_case,
            "expected_gdp": expected_case,
            "worst_case_gdp": worst_case
        }
