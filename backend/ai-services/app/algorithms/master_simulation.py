import sys
import os
import concurrent.futures
from typing import Dict, Any

# Append paths to allow importing from submodules
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the 'app' directory to sys.path so that absolute imports work regardless of where the script is run from
app_dir = os.path.dirname(current_dir)
if app_dir not in sys.path:
    sys.path.append(app_dir)

# Also append subdirectories so legacy internal imports (e.g. `from rk4 import RK4Integrator`) still work
sys.path.append(os.path.join(current_dir, 'system_dynamics'))
sys.path.append(os.path.join(current_dir, 'gnn'))
sys.path.append(os.path.join(current_dir, 'abm'))
sys.path.append(os.path.join(current_dir, 'finance'))

from algorithms.system_dynamics.macro_model import MacroEnvironment
from algorithms.system_dynamics.world_network import WorldNetwork
from algorithms.gnn.geopolitics_model import GeopoliticsModel
from algorithms.abm.world import WorldEnvironment
from algorithms.abm.agent import VirtualCitizen
from algorithms.finance.market_engine import FinancialMarketEngine
from algorithms.events.event_engine import EventEngine, WarEvent, PandemicEvent, EnergyCrisisEvent
from algorithms.models.rl_agent import PolicyRLAgent
from algorithms.abm.company import CorporateEngine
from algorithms.system_dynamics.supply_chain import SupplyChainEngine
from algorithms.system_dynamics.energy_model import EnergyEngine
from algorithms.nlp.news_generator import NLPNewsGenerator
from algorithms.finance.central_bank import CentralBank
from algorithms.models.monte_carlo import MonteCarloEngine

class MasterSimulation:
    def __init__(self):
        print("Initializing Master World Simulation Engine (Digital Twin Earth Scale)...")
        
        # 1. Global Network (195 Nations)
        self.world_network = WorldNetwork()
        self.macro = MacroEnvironment() # Kept for backward compat with EventEngine impacts
        
        # 2. Politics
        self.geopolitics = GeopoliticsModel()
        
        # 3. Society (ABM)
        self.world = WorldEnvironment(width=20, height=20)
        self.event_engine = EventEngine()
        
        # Add some citizens
        for i in range(5):
            agent = VirtualCitizen(agent_id=i, x=10, y=10, world=self.world)
            self.world.add_agent(agent)
            
        # 4. Finance
        self.finance = FinancialMarketEngine()
        
        # 5. RL Policy Engine
        self.rl_policy_engine = PolicyRLAgent()
        
        # 4. Central Bank & Monte Carlo Scenario Engine
        self.central_bank = CentralBank()
        self.monte_carlo = MonteCarloEngine()
        
        # 5. Energy and Resource Modelsy Chain
        self.corporate = CorporateEngine()
        self.supply_chain = SupplyChainEngine()
        
        # 7. Energy & Climate
        self.energy = EnergyEngine(gdp=300000.0)
        
        # 8. News & NLP
        self.news_nlp = NLPNewsGenerator()

    def run_tick(self, tick: int):
        print(f"\n=========================================\nSIMULATION TICK {tick}\n=========================================")
        
        # --- STEP 0: EVENT ENGINE ---
        print("\n[Step 0: Global Events]")
        # Example: Trigger an Energy Crisis randomly (or based on some logic)
        import random
        if tick == 2:
            self.event_engine.trigger_event(EnergyCrisisEvent("Global Oil Shock", severity=8.0))
        if tick == 3:
            self.event_engine.trigger_event(WarEvent("Regional Conflict", severity=7.0, regions_involved=["Middle East"]))
            
        # Get impacts from active events
        global_state: Dict[str, Any] = self.world_network.get_global_state() # type: ignore
        event_impacts = self.event_engine.get_aggregated_impacts(global_state)
        if event_impacts:
            print(f"Active Event Impacts: {event_impacts}")
            
            # Apply localized impacts to NationStates
            affected = random.sample(list(self.world_network.nations.values()), min(5, len(self.world_network.nations)))
            
            for nation in affected:
                if "manufacturing_output_modifier" in event_impacts:
                    nation.economy.F[1] *= (1.0 + event_impacts["manufacturing_output_modifier"])
                if "agriculture_output_modifier" in event_impacts:
                    nation.economy.F[0] *= (1.0 + event_impacts["agriculture_output_modifier"])
                if "technology_output_modifier" in event_impacts:
                    nation.economy.F[2] *= (1.0 + event_impacts["technology_output_modifier"])
                if "inflation_spike" in event_impacts:
                    nation.interest_rate += event_impacts["inflation_spike"] * 0.1 # Reaction to inflation
                    
            if "market_drift_modifier" in event_impacts:
                self.macro.market_drift += event_impacts["market_drift_modifier"]
            if "market_volatility_modifier" in event_impacts:
                self.macro.market_vol += event_impacts["market_volatility_modifier"]
            if "oil_price_spike" in event_impacts:
                # Store globally for other systems
                global_state["oil_price_modifier"] = global_state.get("oil_price_modifier", 0.0) + event_impacts["oil_price_spike"]
            if "trade_disruption" in event_impacts:
                global_state["trade_friction"] = global_state.get("trade_friction", 0.0) + event_impacts["trade_disruption"]
                self.supply_chain.apply_shock("Shanghai_Port", min(0.9, event_impacts["trade_disruption"]))

        # --- STEP 1: MACRO-ECONOMY & CLIMATE ---
        print("\n[Step 1: Macro-Economy & Climate (Digital Twin Scale)]")
        self.world_network.tick()
        global_state: Dict[str, Any] = self.world_network.get_global_state() # type: ignore
        print(f"Global Aggregated State: {global_state}")
        
        # Geopolitical Step needs economic health as input
        # Calculate a proxy for global economic health from aggregated GDP
        total_output = global_state.get("total_gdp", 1000)
        economic_health = float(total_output) / 100000.0 # Normalize
        
        # --- STEP 1.5: ENERGY, SUPPLY CHAIN & CORPORATE ---
        print("\n[Step 1.5: Energy, Supply Chain, and Corporate Sectors]")
        gdp_growth = global_state.get('gdp_growth', 0.02) # proxy if doesn't exist
        
        # Energy Engine (Fossil to Renewable, CO2 emissions)
        energy_results = self.energy.step(gdp_growth=gdp_growth, crisis_impacts=global_state)
        global_state['total_co2'] = energy_results['co2_emissions']
        print(f"   Energy Grid Status: Shortfall={energy_results['shortfall']:.1f}, CO2 Emitted={energy_results['co2_emissions']:.1f}")
        
        # Supply Chain Engine (Ports and Logistics)
        sc_results = self.supply_chain.step(global_demand_factor=1.0 + gdp_growth)
        print(f"   Supply Chain Health: Overall={sc_results['supply_chain_health']*100:.1f}% | Ports={sc_results['port_health']*100:.1f}% | Air={sc_results['air_health']*100:.1f}% | Rail={sc_results['rail_health']*100:.1f}%")
        
        # Corporate Engine (Apple, Microsoft, etc)
        corp_results = self.corporate.step(global_state)
        print("   Corporate Sector Agents:")
        for res in corp_results:
            print(f"      - {res['name']} ({res['sector']}): Rev ${res['revenue']/1e9:.2f}B | Mkt Share: {res['market_share']*100:.1f}% | Cash: ${res['cash_reserves']/1e9:.2f}B")
        total_corp_revenue = sum(c['revenue'] for c in corp_results if c['status'] == 'Active')
        
        # Re-inject corporate wealth into global state
        global_state['total_gdp'] += total_corp_revenue * 0.01 # proxy for corporate value add
        
        # --- NLP LIVE NEWS FEED ---
        print("\n[Global News Feed (NLP)]")
        news_state = {
            "gdp_growth": gdp_growth, 
            "total_infected": global_state.get("total_infected", 0), 
            "active_events": self.event_engine.active_events
        }
        headlines = self.news_nlp.generate_news(news_state)
        for h in headlines:
            print(f" - NEWS: {h}")

        # --- STEP 2: POLITICS & GOVERNMENT ---
        print("\n[Step 2: Geopolitics, Alliances & Dynamic Government Policies]")
        
        # Apply dynamic policies per nation
        def apply_nation_policy(nation):
            gdp_health = nation.gdp / 1000.0
            inflation = getattr(nation, 'inflation', 0.02) # Default if missing
            infection_rate = nation.health.I / nation.population if nation.population > 0 else 0
            has_war = any(e.__class__.__name__ == 'WarEvent' for e in self.event_engine.active_events)
            has_crisis = any("Crisis" in e.__class__.__name__ for e in self.event_engine.active_events)
            
            # Use RL Policy Engine to pick optimal tax and interest rates
            action_dict, action_idx, state = self.rl_policy_engine.choose_action(gdp_growth=gdp_health-1.0, inflation=inflation)
            
            # Apply dynamic changes incrementally
            nation.tax_rate = max(0.0, min(0.5, nation.tax_rate + action_dict["tax"]))
            nation.interest_rate = self.central_bank.interest_rate
            if has_crisis:
                nation.interest_rate += 0.02
                
            if infection_rate > 0.05:
                nation.subsidies = nation.gdp * 0.05
            else:
                nation.subsidies = 0.0
                
            if has_war:
                nation.military_spending_pct = 0.10
            else:
                nation.military_spending_pct = 0.02

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(apply_nation_policy, self.world_network.nations.values())
                
        # Central Bank Step
        cb_res = self.central_bank.step(current_inflation=0.02, gdp_growth=gdp_growth)
        print(f"   Central Bank Policy: Target Interest Rate={cb_res['interest_rate']*100:.2f}%, QE Active={cb_res['qe_active']}, M2 Supply=${cb_res['money_supply_b']:,.1f}B")

        # Set an average global tax for the ABM citizens
        avg_tax = sum(n.tax_rate for n in self.world_network.nations.values()) / max(1, len(self.world_network.nations))
        self.world.global_tax_rate = avg_tax
        print(f"Global Average Tax Rate set to {avg_tax*100:.1f}%")
        
        # Geopolitics (PageRank, GNN, BBN, MDP, HMM)
        global_gdp = global_state.get('total_gdp', 300000.0)
        self.geopolitics.run_analysis(active_events=self.event_engine.active_events, global_gdp=global_gdp)
        
        # --- STEP 3: SOCIETY (ABM) ---
        print(f"\n[Step 3: Society (Agents)] -> Global Tax Rate set to {avg_tax*100}%")
        
        # Climate impacts Society: High CO2 increases infection risk
        # global_state keys: total_gdp, total_co2, total_infected
        max_co2 = global_state.get("total_co2", 100.0) / len(self.world_network.nations) # Avg CO2 per nation
        if max_co2 > 1500.0:
            print("CLIMATE ALERT: High CO2 levels detected! Infection spreading.")
            self.world.cellular.set_state(10, 10, 1.0) # Seed infection
            
        self.world.tick()
        
        # --- STEP 4: FINANCE ---
        print(f"\n[Step 4: Financial Markets]")
        
        # Construct 5D Macro Context for LSTM (GDP, Inflation, Interest Rate, CO2)
        macro_context = [
            global_state.get("total_gdp", 100.0),
            avg_tax * 0.1, # proxy inflation
            avg_tax * 0.5, # proxy interest
            global_state.get("total_co2", 400.0)
        ]
        finance_results = self.finance.run_market_simulation(
            active_events=self.event_engine.active_events, 
            macro_context=macro_context,
            news_feed=headlines
        )
        global_state['finance_results'] = finance_results
        global_state['headlines'] = headlines
        
        shock_penalty = event_impacts.get("trade_disruption", 0.0)
        print(f"   Event Shock Severity Modifier: {shock_penalty:.2f}")
        
        # --- STEP 5: MONTE CARLO SCENARIOS ---
        print("\n[Step 5: Monte Carlo Scenario Engine]")
        mc_res = self.monte_carlo.run_scenarios(base_gdp=total_output, base_volatility=0.15, active_shocks=shock_penalty)
        print(f"   Ran {mc_res['num_simulations']} simultaneous universe projections for {mc_res['days_forecasted']} days.")
        print(f"   Worst Case (5th Percentile): ${mc_res['worst_case_gdp']:,.2f}")
        print(f"   Expected Case (Median): ${mc_res['expected_gdp']:,.2f}")
        print(f"   Best Case (95th Percentile): ${mc_res['best_case_gdp']:,.2f}")
        
        # --- MLOPS TRACKING ---
        # Temporarily disabled to prevent urllib3 retries from blocking the simulation loop
        # import mlflow # type: ignore
        # mlflow.set_tracking_uri("http://localhost:5000") # or internal container URL
        # try:
        #     with mlflow.start_run(run_name=f"Tick_{tick}", nested=True):
        #         mlflow.log_metric("global_gdp", float(total_output))
        #         mlflow.log_metric("market_index", self.macro.market_index)
        #         mlflow.log_metric("co2_ppm", float(max_co2))
        #         mlflow.log_metric("active_events", len(self.event_engine.active_events))
        # except Exception as e:
        #     print(f"MLflow tracking skipped/failed: {e}")

if __name__ == "__main__":
    sim = MasterSimulation()
    for tick in range(1, 4): # Run for 3 ticks
        sim.run_tick(tick)
