class BayesianBeliefNetwork:
    """
    A simple Bayesian Belief Network (BBN) exact inference engine.
    Used to infer the probability of geopolitical events.
    """
    def __init__(self):
        # Stores Conditional Probability Tables (CPTs)
        # Format: { 'Event': { ('Parent1_State', 'Parent2_State'): Probability_True } }
        self.cpts = {}
        self.parents = {} # { 'Event': ['Parent1', 'Parent2'] }
        
    def add_node(self, node, parents, cpt):
        self.parents[node] = parents
        self.cpts[node] = cpt
        
    def query_probability(self, node, parent_states: tuple):
        """
        Get the probability of 'node' being True given the states of its parents.
        """
        if node not in self.cpts:
            return 0.0
            
        # If root node (no parents)
        if not self.parents[node]:
            return self.cpts[node]
            
        return self.cpts[node].get(parent_states, 0.0)

def setup_geopolitics_bbn():
    """
    Helper to create a standard BBN for Global Crisis prediction.
    """
    bbn = BayesianBeliefNetwork()
    
    # Root Nodes (Priors)
    bbn.add_node("Oil_Crash", [], 0.2) # 20% chance inherently
    bbn.add_node("Sanctions", [], 0.3)
    
    # Child Node: Global_Recession depends on Oil_Crash and Sanctions
    # CPT Tuple Order: (Oil_Crash_State, Sanctions_State)
    recession_cpt = {
        (True, True): 0.95,
        (True, False): 0.70,
        (False, True): 0.60,
        (False, False): 0.10
    }
    bbn.add_node("Global_Recession", ["Oil_Crash", "Sanctions"], recession_cpt)
    
    return bbn
