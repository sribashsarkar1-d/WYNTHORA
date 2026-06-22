import numpy as np
import pandas as pd # type: ignore
import concurrent.futures
from nation_state import NationState # type: ignore

class WorldNetwork:
    """
    Manages the 195+ node network of NationStates, handling the trade matrices 
    and global aggregation of economic/climate stats.
    """
    def __init__(self):
        self.nations = {}
        self.trade_matrix = None
        self.iso_list = []
        self._initialize_nations()
        
    def _initialize_nations(self):
        """
        Loads countries from the database. 
        Falls back to generating 195 countries if DB is unavailable.
        """
        try:
            from sqlalchemy import create_engine
            engine = create_engine("postgresql://sribash:56789@localhost:5432/world_sim")
            
            # Fetch latest data for each country
            query = """
            SELECT c.iso_code, c.name as country_name,
                   (SELECT gdp_usd FROM economic_time_series e WHERE e.iso_code = c.iso_code ORDER BY time DESC LIMIT 1) as gdp,
                   (SELECT total_population FROM population_data p WHERE p.iso_code = c.iso_code ORDER BY time DESC LIMIT 1) as pop
            FROM countries c
            """
            df = pd.read_sql(query, engine)
            if len(df) == 0:
                raise ValueError("Empty countries table")
                
            for _, row in df.iterrows():
                iso = row['iso_code']
                name = row['country_name']
                # Use real stats if available, else default fallback
                base_gdp = float(row['gdp']) / 1e9 if pd.notna(row['gdp']) else 1000.0 # Convert to Billions for scale
                pop = int(row['pop']) if pd.notna(row['pop']) else 10_000_000
                
                self.nations[iso] = NationState(iso, name, base_gdp=base_gdp, population=pop)
                self.iso_list.append(iso)
            print(f"WorldNetwork: Loaded {len(self.nations)} nations from database with real World Bank data.")
            
        except Exception as e:
            print(f"WorldNetwork: DB load failed ({e}). Generating 195 simulated nations.")
            for i in range(1, 196):
                iso = f"C{i:03d}"
                name = f"Nation_{i}"
                self.nations[iso] = NationState(iso, name, base_gdp=np.random.uniform(100, 5000), population=np.random.randint(1_000_000, 100_000_000))
                self.iso_list.append(iso)
                
        # Initialize an NxN trade connectivity matrix (edge weights)
        num_nodes = len(self.nations)
        # Random base trade network where nodes are sparsely connected
        self.base_trade_matrix = np.random.rand(num_nodes, num_nodes)
        self.base_trade_matrix = np.where(self.base_trade_matrix > 0.8, self.base_trade_matrix, 0) # 20% sparsity
        np.fill_diagonal(self.base_trade_matrix, 0) # No self-trade loops in this matrix
        
        self.trade_matrix = np.copy(self.base_trade_matrix)
        self.exports = np.zeros(num_nodes)
        self.imports = np.zeros(num_nodes)
        
    def update_trade_network(self):
        """
        Adjusts the trade matrix based on dynamic tariffs and trade agreements.
        """
        if self.trade_matrix is None:
            return
            
        for i, iso_i in enumerate(self.iso_list):
            nation_i = self.nations[iso_i]
            for j, iso_j in enumerate(self.iso_list):
                if i == j: continue
                nation_j = self.nations[iso_j]
                
                base_affinity = self.base_trade_matrix[i, j]
                
                # Tariffs act as trade friction (using tax_rate as a proxy for protectionism)
                tariff_friction = (nation_i.tax_rate + nation_j.tax_rate) / 2.0
                
                # Trade agreements boost trade affinity
                boost = 0.0
                if "Free Trade Expansion" in nation_i.trade_agreements and "Free Trade Expansion" in nation_j.trade_agreements:
                    boost = 0.15
                    
                self.trade_matrix[i, j] = max(0.0, base_affinity * (1.0 - tariff_friction) + boost)
        
    def tick(self):
        """
        Advances the global network by one tick.
        """
        global_co2 = sum(n.co2_emissions for n in self.nations.values())
        
        def process_nation(nation):
            nation.tick(global_co2)
            
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_nation, self.nations.values())
            
        # Simplified Trade Impact:
        # A portion of GDP flows along the trade matrix edges
        if self.trade_matrix is None:
            return
            
        self.update_trade_network()
            
        gdp_array = np.array([n.gdp for n in self.nations.values()])
        
        # Calculate Import/Export Matrix
        # exports_matrix[i, j] = exports from j to i
        exports_matrix = self.trade_matrix * gdp_array # Broadcasts across columns
        
        self.exports = np.sum(exports_matrix, axis=0) # Total exported by j
        self.imports = np.sum(exports_matrix, axis=1) # Total imported by i
        
        net_exports = self.exports - self.imports
        
        # Distribute trade flow back to GDP (GDP = C + I + G + NX)
        for i, iso in enumerate(self.iso_list):
            # Scale net exports impact to avoid wild swings
            self.nations[iso].gdp += net_exports[i] * 0.02
            
    def get_global_state(self):
        """
        Aggregates global metrics.
        """
        total_gdp = sum(n.gdp for n in self.nations.values())
        total_co2 = sum(n.co2_emissions for n in self.nations.values())
        total_infected = sum(n.health.I for n in self.nations.values())
        
        return {
            "total_gdp": total_gdp,
            "total_co2": total_co2,
            "total_infected": total_infected,
            "num_nations": len(self.nations)
        }
