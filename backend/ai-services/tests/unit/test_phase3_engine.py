import pytest
import asyncio
import time
from app.simulation.states.global_state import SimulationStateStore
from app.simulation.engine.core import AsyncSimulationEngine
from app.domains.economy.system_dynamics.world_network import WorldNetwork
from app.domains.population.abm.world import WorldEnvironment

@pytest.mark.asyncio
async def test_state_integrity():
    store = SimulationStateStore()
    
    # Test initial values
    val = await store.get("global_gdp")
    assert val == 100000.0
    
    # Test concurrent writes
    async def writer_1():
        await store.set("temperature", 20.0)
        
    async def writer_2():
        await store.update({"crises": ["flood"], "temperature": 25.0})
        
    await asyncio.gather(writer_1(), writer_2())
    
    state = await store.get_all()
    assert state["temperature"] in [20.0, 25.0]
    assert "flood" in state["crises"]

@pytest.mark.asyncio
async def test_async_engine_concurrency():
    engine = AsyncSimulationEngine()
    
    # Instantiate real domains
    economy = WorldNetwork()
    abm = WorldEnvironment(width=10, height=10)
    
    engine.register_domain(economy)
    engine.register_domain(abm)
    
    await engine.initialize()
    
    start_time = time.time()
    # Run 2 ticks
    await engine.run_simulation(total_ticks=2)
    end_time = time.time()
    
    # Verify state updates correctly (WorldNetwork updates total_gdp)
    final_state = await engine.state_store.get_all()
    assert final_state["current_tick"] == 2
    assert "total_gdp" in final_state
    
    # Print metrics
    print(f"Async Engine 2 Ticks took {end_time - start_time:.4f} seconds.")
    print(f"Final State: {final_state}")
