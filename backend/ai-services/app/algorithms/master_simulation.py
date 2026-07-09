import sys
import os
import concurrent.futures
from typing import Dict, Any
import logging
from enum import Enum, auto

# Append paths to allow importing from submodules
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
if app_dir not in sys.path:
    sys.path.append(app_dir)

sys.path.append(os.path.join(current_dir, 'system_dynamics'))
sys.path.append(os.path.join(current_dir, 'gnn'))
sys.path.append(os.path.join(current_dir, 'abm'))
sys.path.append(os.path.join(current_dir, 'finance'))

from app.algorithms.system_dynamics.macro_model import MacroEnvironment
from app.algorithms.system_dynamics.world_network import WorldNetwork
from app.algorithms.gnn.geopolitics_model import GeopoliticsModel
from app.algorithms.abm.world import WorldEnvironment
from app.algorithms.abm.agent import VirtualCitizen
from app.algorithms.finance.market_engine import FinancialMarketEngine
from app.algorithms.events.event_engine import EventEngine, WarEvent, PandemicEvent, EnergyCrisisEvent
from app.algorithms.models.rl_agent import PolicyRLAgent
from app.algorithms.abm.company import CorporateEngine
from app.algorithms.system_dynamics.supply_chain import SupplyChainEngine
from app.algorithms.system_dynamics.energy_model import EnergyEngine
from app.algorithms.nlp.news_generator import NLPNewsGenerator
from app.algorithms.finance.central_bank import CentralBank
from app.algorithms.models.monte_carlo import MonteCarloEngine
from app.algorithms.data_loader import RealWorldDataLoader
import asyncio

logger = logging.getLogger("MasterSimulation")

class SimulationState(Enum):
    INIT = auto()
    LOADING_DATA = auto()
    RUNNING = auto()
    PAUSED = auto()
    ERROR = auto()

class SimulationFSM:
    def __init__(self):
        self.state = SimulationState.INIT
        
    def transition_to(self, new_state: SimulationState):
        logger.info(f"FSM State Transition: {self.state.name} -> {new_state.name}")
        self.state = new_state

class MasterSimulation:
    def __init__(self):
        self.fsm = SimulationFSM()
        logger.info("Initializing Master World Simulation Engine (Digital Twin Earth Scale)...")
        
        # 0. Real Data Loader
        self.data_loader = RealWorldDataLoader()
        
        # 1. Global Network (195 Nations)
        self.world_network = WorldNetwork()
        self.macro = MacroEnvironment()
        
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
        self.rl_policy_engine = PolicyRLAgent()
        self.central_bank = CentralBank()
        self.monte_carlo = MonteCarloEngine()
        
        # 5. Energy and Resource Models
        self.corporate = CorporateEngine()
        self.supply_chain = SupplyChainEngine()
        self.energy = EnergyEngine(gdp=300000.0)
        
        # 6. News & NLP
        self.news_nlp = NLPNewsGenerator()
        
    async def initialize_data(self):
        self.fsm.transition_to(SimulationState.LOADING_DATA)
        try:
            imf_data = await self.data_loader.fetch_imf_data()
            climate_data = await self.data_loader.fetch_noaa_climate()
            await self.geopolitics.initialize_data()
            await self.finance.initialize_data()
            logger.info(f"Loaded Real Data: IMF={imf_data}, Climate={climate_data}")
            self.fsm.transition_to(SimulationState.RUNNING)
        except Exception as e:
            logger.error(f"Failed to initialize data: {e}")
            self.fsm.transition_to(SimulationState.ERROR)
            raise

    def run_tick(self, tick: int):
        if self.fsm.state != SimulationState.RUNNING:
            logger.warning(f"Cannot run tick {tick} while in state {self.fsm.state.name}")
            return
            
        logger.info(f"================ SIMULATION TICK {tick} ================")
        
        try:
            # --- STEP 0: EVENT ENGINE ---
            import random
            if tick == 2:
                self.event_engine.trigger_event(EnergyCrisisEvent("Global Oil Shock", severity=8.0))
            if tick == 3:
                self.event_engine.trigger_event(WarEvent("Regional Conflict", severity=7.0, regions_involved=["Middle East"]))
                
            global_state: Dict[str, Any] = self.world_network.get_global_state() # type: ignore
            event_impacts = self.event_engine.get_aggregated_impacts(global_state)
            
            if event_impacts:
                affected = random.sample(list(self.world_network.nations.values()), min(5, max(1, len(self.world_network.nations))))
                for nation in affected:
                    if "manufacturing_output_modifier" in event_impacts:
                        nation.economy.F[1] *= (1.0 + event_impacts["manufacturing_output_modifier"])
                    if "inflation_spike" in event_impacts:
                        nation.interest_rate += event_impacts["inflation_spike"] * 0.1
                        
                if "market_drift_modifier" in event_impacts:
                    self.macro.market_drift += event_impacts["market_drift_modifier"]
                if "market_volatility_modifier" in event_impacts:
                    self.macro.market_vol += event_impacts["market_volatility_modifier"]

            # --- STEP 1: MACRO-ECONOMY & CLIMATE ---
            self.world_network.tick()
            global_state = self.world_network.get_global_state() # type: ignore
            total_output = global_state.get("total_gdp", 1000)
            
            # --- STEP 1.5: ENERGY, SUPPLY CHAIN & CORPORATE ---
            gdp_growth = global_state.get('gdp_growth', 0.02)
            energy_results = self.energy.step(gdp_growth=gdp_growth, crisis_impacts=global_state)
            global_state['total_co2'] = energy_results['co2_emissions']
            
            sc_results = self.supply_chain.step(global_demand_factor=1.0 + gdp_growth)
            corp_results = self.corporate.step(global_state)
            
            # --- NLP LIVE NEWS FEED ---
            news_state = {
                "gdp_growth": gdp_growth, 
                "total_infected": global_state.get("total_infected", 0), 
                "active_events": self.event_engine.active_events
            }
            headlines = self.news_nlp.generate_news(news_state)

            # --- STEP 2: POLITICS & GOVERNMENT ---
            def apply_nation_policy(nation):
                gdp_health = nation.gdp / 1000.0
                inflation = getattr(nation, 'inflation', 0.02)
                action_dict, _, _ = self.rl_policy_engine.choose_action(gdp_growth=gdp_health-1.0, inflation=inflation)
                nation.tax_rate = max(0.0, min(0.5, nation.tax_rate + action_dict["tax"]))
                nation.interest_rate = self.central_bank.interest_rate

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(apply_nation_policy, self.world_network.nations.values())
                    
            cb_res = self.central_bank.step(current_inflation=0.02, gdp_growth=gdp_growth)
            avg_tax = sum(n.tax_rate for n in self.world_network.nations.values()) / max(1, len(self.world_network.nations))
            self.world.global_tax_rate = avg_tax
            
            self.geopolitics.run_analysis(active_events=self.event_engine.active_events, global_gdp=total_output)
            
            # --- STEP 3: SOCIETY (ABM) ---
            max_co2 = global_state.get("total_co2", 100.0) / max(1, len(self.world_network.nations))
            if max_co2 > 1500.0:
                self.world.cellular.set_state(10, 10, 1.0)
            self.world.tick()
            
            # --- STEP 4: FINANCE & MONTE CARLO ---
            macro_context = [
                global_state.get("total_gdp", 100.0),
                avg_tax * 0.1,
                avg_tax * 0.5,
                global_state.get("total_co2", 400.0)
            ]
            finance_results = self.finance.run_market_simulation(
                active_events=self.event_engine.active_events, 
                macro_context=macro_context,
                news_feed=headlines
            )
            
            shock_penalty = event_impacts.get("trade_disruption", 0.0) if event_impacts else 0.0
            mc_res = self.monte_carlo.run_scenarios(base_gdp=total_output, base_volatility=0.15, active_shocks=shock_penalty)
            
        except Exception as e:
            logger.error(f"Simulation Error at tick {tick}: {e}")
            self.fsm.transition_to(SimulationState.ERROR)

async def main():
    sim = MasterSimulation()
    await sim.initialize_data()
    for tick in range(1, 4):
        sim.run_tick(tick)

if __name__ == "__main__":
    asyncio.run(main())
