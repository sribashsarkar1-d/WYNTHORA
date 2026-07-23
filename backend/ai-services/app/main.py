from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from app.core.logging import setup_logging
from app.core.telemetry import setup_telemetry

logger = setup_logging()

from app.api.v1.endpoints import simulation
from app.simulation.engine.core import AsyncSimulationEngine
from app.domains.economy.system_dynamics.world_network import WorldNetwork
from app.domains.population.abm.world import WorldEnvironment

async def simulation_worker(app: FastAPI):
    logger.info("Background Async Simulation Worker Started")
    from app.api.v1.endpoints.simulation import manager
    
    engine: AsyncSimulationEngine = app.state.engine
    tick_counter = 1
    
    while app.state.is_running:
        try:
            await engine.run_tick(tick_counter)
            
            # Fetch latest state to broadcast
            latest_state = await engine.state_store.get_all()
            
            # Broadcast live state to all WebSocket clients
            await manager.broadcast({
                "tick": latest_state.get("current_tick", tick_counter),
                "status": "Running",
                "global_gdp": float(latest_state.get("total_gdp", 0) / 1000),
                "co2_ppm": float(latest_state.get("total_co2", 0) / 195),
                "active_events": latest_state.get("active_crises", []),
                "abm_active_agents": latest_state.get("abm_active_agents", 0),
                "last_tick_duration": latest_state.get("last_tick_duration_seconds", 0.0)
            })
            
            tick_counter += 1
            await asyncio.sleep(2) # 2 seconds per tick to simulate real-time feel
            
        except Exception as e:
            logger.error(f"Error in simulation worker: {e}")
            await asyncio.sleep(5) # Backoff on error

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing Simulation Engine and Domains...")
    engine = AsyncSimulationEngine()
    
    # Register Domains
    world_network = WorldNetwork()
    abm_world = WorldEnvironment(width=10, height=10)
    engine.register_domain(world_network)
    engine.register_domain(abm_world)
    
    await engine.initialize()
    
    # Store globally
    app.state.engine = engine
    app.state.is_running = True
    
    # Start the async background worker
    worker_task = asyncio.create_task(simulation_worker(app))
    
    yield
    
    # Shutdown
    app.state.is_running = False
    worker_task.cancel()
    logger.info("Simulation Engine Shutdown Complete.")

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.api.v1.endpoints.simulation import limiter

app = FastAPI(title="AI Services API - Enterprise Edition", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

# Setup Telemetry
setup_telemetry(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router, prefix="/api/v1/simulation")

@app.get("/api/ai/health")
def health_check():
    return {"status": "AI Services Engine is running"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
