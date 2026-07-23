class CobbDouglasUtility:
    """
    Implements Cobb-Douglas Utility Function: U(X, Y) = A * X^alpha * Y^beta
    Used to calculate optimal resource allocation for an agent.
    """
    def __init__(self, A=1.0):
        self.A = A
        self.preferences = {} # { item_name: alpha_value }

    def set_preference(self, item_name, elasticity):
        """
        Sets the elasticity parameter (alpha/beta) for an item.
        Higher elasticity means the agent prefers this item more.
        """
        self.preferences[item_name] = elasticity

    def calculate_utility(self, inventory: dict):
        """
        Calculates total utility given a dictionary of item quantities.
        """
        utility = self.A
        for item, qty in inventory.items():
            alpha = self.preferences.get(item, 0.0)
            if alpha > 0:
                # Avoid log/math domain errors by ensuring qty > 0 if alpha > 0
                utility *= (max(qty, 0.01) ** alpha)
        return utility

    def optimal_basket(self, budget, prices: dict):
        """
        Calculates the theoretical optimal amount of goods to buy given a budget and prices.
        Assumes the agent wants to maximize utility using all their budget.
        Returns { item_name: quantity_to_buy }
        """
        # Sum of all alphas (elasticities)
        total_alpha = sum(self.preferences.values())
        if total_alpha == 0:
            return {item: 0.0 for item in prices}

        optimal = {}
        for item, price in prices.items():
            if item in self.preferences and price > 0:
                alpha = self.preferences[item]
                # Formula: x_i = (alpha_i / sum(alphas)) * (Budget / Price_i)
                optimal_qty = (alpha / total_alpha) * (budget / price)
                optimal[item] = optimal_qty
            else:
                optimal[item] = 0.0
                
        return optimal
