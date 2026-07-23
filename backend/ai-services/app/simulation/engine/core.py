import asyncio
import logging
import time
from typing import Dict, Any
from app.simulation.states.global_state import SimulationStateStore

logger = logging.getLogger("AsyncSimulationEngine")

class AsyncSimulationEngine:
    """
    The master asynchronous orchestrator for the World Simulation.
    Replaces the legacy synchronous master_simulation.py.
    """
    def __init__(self):
        self.state_store = SimulationStateStore()
        
        # In a real setup, these would be injected instances of actual domains.
        # For Phase 3 core refactoring, we prepare the interfaces and dummy runners.
        self.domains = []
        
    def register_domain(self, domain_runner: Any):
        """
        Registers a domain (e.g. Economy, Politics) that must have an async tick() method.
        """
        self.domains.append(domain_runner)
        
    async def initialize(self):
        logger.info("Initializing Async Simulation Engine...")
        await self.state_store.set("simulation_status", "INITIALIZED")
        
    async def run_tick(self, tick_id: int):
        logger.info(f"--- TICK {tick_id} START ---")
        start_time = time.time()
        
        # Execute all registered domains concurrently
        tasks = []
        for domain in self.domains:
            # We pass the state_store so domains can read/write global context
            tasks.append(domain.tick(self.state_store))
            
        # Gather results (if any exceptions occur, return_exceptions=False crashes early, which is preferred for now)
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Update tick metadata in the state store
        await self.state_store.update({
            "current_tick": tick_id,
            "last_tick_duration_seconds": elapsed
        })
        
        logger.info(f"--- TICK {tick_id} END ({elapsed:.4f}s) ---")
        
    async def run_simulation(self, total_ticks: int = 10):
        await self.initialize()
        for i in range(1, total_ticks + 1):
            await self.run_tick(i)
            # In a real engine, we might sleep to sync with real-time or just run as fast as possible.
            await asyncio.sleep(0.01) 
