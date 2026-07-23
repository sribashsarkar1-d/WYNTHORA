import math

def norm_cdf(x):
    """Cumulative distribution function for the standard normal distribution."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

class BlackScholesPricer:
    """
    Computes theoretical prices of European Call and Put options.
    """
    def __init__(self, risk_free_rate=0.05):
        self.r = risk_free_rate

    def price(self, S, K, T, sigma, option_type='call'):
        """
        S: Current Stock Price
        K: Strike Price
        T: Time to maturity (in years)
        sigma: Volatility of the underlying asset
        option_type: 'call' or 'put'
        """
        if T <= 0:
            return max(0.0, S - K) if option_type == 'call' else max(0.0, K - S)

        d1 = (math.log(S / K) + (self.r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        if option_type == 'call':
            price = S * norm_cdf(d1) - K * math.exp(-self.r * T) * norm_cdf(d2)
        elif option_type == 'put':
            price = K * math.exp(-self.r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        else:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")

        return price
