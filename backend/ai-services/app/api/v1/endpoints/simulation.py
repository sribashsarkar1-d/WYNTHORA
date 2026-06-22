from fastapi import APIRouter, Depends, HTTPException, Security, status, Request, WebSocket, WebSocketDisconnect
from fastapi.security.api_key import APIKeyHeader
import logging
import asyncio
from algorithms.events.event_engine import WarEvent, PandemicEvent, EnergyCrisisEvent
from algorithms.nlp.news_generator import NLPNewsGenerator

router = APIRouter()
logger = logging.getLogger("API_Simulation")
news_gen = NLPNewsGenerator()

API_KEY = "enterprise-secret-key-2026"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Live streaming WebSocket endpoint for the Digital Twin simulation state.
    """
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from the client in this one-way stream,
            # but we need to receive to keep the connection alive and detect disconnects.
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- Existing HTTP Endpoints ---

@router.get("/status", tags=["Dashboard"])
async def get_simulation_status(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns the real-time simulation tick, market index, and macroeconomic state.
    """
    sim_state = request.app.state.sim_state
    if not sim_state.sim_instance:
        return {"status": "Starting..."}
        
    return {
        "tick": sim_state.tick,
        "status": "Running" if sim_state.is_running else "Paused",
        "market_index": float(sim_state.sim_instance.macro.market_index),
        "global_gdp": float(sim_state.latest_global_state.get("total_gdp", 0) / 1000), # Scale for UI
        "co2_ppm": float(sim_state.latest_global_state.get("total_co2", 0) / 195),
        "active_events": sim_state.active_events
    }

@router.post("/events/trigger", tags=["Control Panel"])
async def trigger_event(request: Request, event_name: str, severity: float, api_key: str = Depends(get_api_key)):
    """
    Triggers a global event dynamically in the real engine.
    """
    sim_state = request.app.state.sim_state
    if not sim_state.sim_instance:
        raise HTTPException(status_code=503, detail="Simulation not ready")
        
    if "War" in event_name:
        evt = WarEvent(event_name, severity, ["Random Region"])
    elif "Crisis" in event_name or "Shock" in event_name:
        evt = EnergyCrisisEvent(event_name, severity)
    else:
        evt = PandemicEvent(event_name, severity)
        
    sim_state.sim_instance.event_engine.trigger_event(evt)
    logger.info(f"Triggered real event {event_name} via API")
    return {"message": f"Event '{event_name}' injected into simulation!"}

@router.get("/forecasts/risk", tags=["Dashboard"])
async def get_risk_forecast(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns AI forecasting outputs.
    """
    sim_state = request.app.state.sim_state
    # Mocking for now as models are too heavy for constant 2s poll
    # In a full production, we would use real model outputs from MasterSimulation
    crash_prob = 0.874 if sim_state.active_events else 0.125
    conflict_risk = 0.95 if any("War" in e for e in sim_state.active_events) else 0.241
    
    return {
        "market_crash_probability": crash_prob,
        "conflict_risk": conflict_risk,
        "sentiment": "Markets panicked!" if sim_state.active_events else "Markets stable."
    }

@router.get("/news", tags=["Dashboard"])
async def get_latest_news(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns AI-generated breaking news based on the real-time simulation state.
    """
    sim_state = request.app.state.sim_state
    
    state_dict = {
        "gdp_growth": 0.05 if sim_state.latest_global_state.get("total_gdp", 0) > 1200 else -0.05,
        "total_infected": sim_state.latest_global_state.get("total_infected", 0),
        "active_events": sim_state.active_events
    }
    
    headlines = news_gen.generate_news(state_dict)
    return {"headlines": headlines}
