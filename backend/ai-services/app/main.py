from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from api.v1.endpoints import simulation
from algorithms.master_simulation import MasterSimulation # type: ignore

# Global Simulation State
class SharedState:
    sim_instance = None
    tick = 0
    is_running = False
    latest_global_state = {
        "total_gdp": 1000.0,
        "total_co2": 400.0,
        "total_infected": 0
    }
    active_events = []

async def simulation_worker():
    print("Background Async Simulation Worker Started")
    loop = asyncio.get_running_loop()
    from api.v1.endpoints.simulation import manager
    
    while True:
        if SharedState.is_running and SharedState.sim_instance:
            SharedState.tick += 1
            
            # run_tick is CPU-bound, so we run it in an executor to avoid blocking the event loop
            await loop.run_in_executor(None, SharedState.sim_instance.run_tick, SharedState.tick)
            
            # Update metrics for API
            SharedState.latest_global_state = SharedState.sim_instance.world_network.get_global_state()
            SharedState.active_events = list(SharedState.sim_instance.event_engine.active_events.keys())
            
            # Broadcast live state to all WebSocket clients
            await manager.broadcast({
                "tick": SharedState.tick,
                "status": "Running",
                "market_index": float(SharedState.sim_instance.macro.market_index),
                "global_gdp": float(SharedState.latest_global_state.get("total_gdp", 0) / 1000),
                "co2_ppm": float(SharedState.latest_global_state.get("total_co2", 0) / 195),
                "active_events": SharedState.active_events,
                "crash_risk": float(SharedState.latest_global_state.get('finance_results', {}).get('crash_risk', 0.125)),
                "sentiment_score": float(SharedState.latest_global_state.get('finance_results', {}).get('sentiment_score', 0.0)),
                "lstm_pred": float(SharedState.latest_global_state.get('finance_results', {}).get('lstm_pred', 0.0)),
                "headlines": SharedState.latest_global_state.get('headlines', [])
            })
            
        await asyncio.sleep(2) # 2 seconds per tick

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    SharedState.sim_instance = MasterSimulation()
    # Auto-start simulation for demo
    SharedState.is_running = True
    
    # Start the async background worker
    worker_task = asyncio.create_task(simulation_worker())
    
    yield
    
    # Shutdown
    worker_task.cancel()
    SharedState.is_running = False

app = FastAPI(title="AI Services API - Enterprise Edition", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inject SharedState into endpoints by passing it via app.state
app.state.sim_state = SharedState

app.include_router(simulation.router, prefix="/api/v1/simulation")

@app.get("/api/ai/health")
def health_check():
    return {"status": "AI Services Engine is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
