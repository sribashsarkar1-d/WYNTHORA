from fastapi import APIRouter, Depends, HTTPException, Security, status, Request, WebSocket, WebSocketDisconnect
from fastapi.security.api_key import APIKeyHeader
import logging
from typing import Dict, Any
import json

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.api.v1.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.algorithms.events.event_engine import WarEvent, PandemicEvent, EnergyCrisisEvent
from app.algorithms.nlp.news_generator import NLPNewsGenerator

router = APIRouter()
logger = logging.getLogger("API_Simulation")
news_gen = NLPNewsGenerator()
limiter = Limiter(key_func=get_remote_address)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.SECRET_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

# --- WebSocket Connection Manager (Phase 16) ---
class ConnectionManager:
    def __init__(self):
        # Maps websocket to their subscribed topics
        self.active_connections: Dict[WebSocket, list] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        # By default, subscribe to 'global' channel
        self.active_connections[websocket] = ["global"]

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: dict, topic: str = "global"):
        for connection, subscriptions in list(self.active_connections.items()):
            if topic in subscriptions:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.warning(f"Failed to send WS message: {e}")
                    self.disconnect(connection)

    async def handle_client_message(self, websocket: WebSocket, text_data: str):
        try:
            data = json.loads(text_data)
            action = data.get("action")
            topic = data.get("topic")
            
            if action == "subscribe" and topic:
                if topic not in self.active_connections[websocket]:
                    self.active_connections[websocket].append(topic)
                await websocket.send_json({"status": "subscribed", "topic": topic})
                
            elif action == "unsubscribe" and topic:
                if topic in self.active_connections[websocket]:
                    self.active_connections[websocket].remove(topic)
                await websocket.send_json({"status": "unsubscribed", "topic": topic})
                
        except json.JSONDecodeError:
            await websocket.send_json({"error": "Invalid JSON payload"})

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Live streaming WebSocket endpoint for the Digital Twin simulation state.
    Supports subscriptions (e.g., {"action": "subscribe", "topic": "news"})
    """
    await manager.connect(websocket)
    try:
        while True:
            text_data = await websocket.receive_text()
            await manager.handle_client_message(websocket, text_data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# --- HTTP Endpoints ---

@router.get("/status", tags=["Dashboard"])
async def get_simulation_status(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns the real-time simulation tick, market index, and macroeconomic state.
    """
    sim_state = getattr(request.app.state, "sim_state", None)
    if not sim_state or not getattr(sim_state, "sim_instance", None):
        return {"status": "Starting or Unavailable"}
        
    return {
        "tick": sim_state.tick,
        "status": "Running" if sim_state.is_running else "Paused",
        "market_index": float(sim_state.sim_instance.macro.market_index),
        "global_gdp": float(sim_state.latest_global_state.get("total_gdp", 0) / 1000),
        "co2_ppm": float(sim_state.latest_global_state.get("total_co2", 0) / 195),
        "active_events": sim_state.active_events
    }

from app.core.security import require_role
from typing import Dict

@router.post("/events/trigger", tags=["Control Panel"])
@limiter.limit("5/minute")
async def trigger_event(
    request: Request, 
    event_name: str, 
    severity: float, 
    api_key: str = Depends(get_api_key),
    user: Dict = Depends(require_role("admin"))
):
    """
    Triggers a global event dynamically in the real engine. (Requires Admin Role)
    """
    if not (1.0 <= severity <= 10.0):
        raise HTTPException(status_code=400, detail="Severity must be between 1.0 and 10.0")

    sim_state = getattr(request.app.state, "sim_state", None)
    if not sim_state or not getattr(sim_state, "sim_instance", None):
        raise HTTPException(status_code=503, detail="Simulation not ready")
        
    try:
        if "War" in event_name:
            evt = WarEvent(event_name, severity, ["Random Region"])
        elif "Crisis" in event_name or "Shock" in event_name:
            evt = EnergyCrisisEvent(event_name, severity)
        else:
            evt = PandemicEvent(event_name, severity)
            
        sim_state.sim_instance.event_engine.trigger_event(evt)
        logger.info(f"Triggered real event {event_name} via API by user {user.get('sub')}")
        return {"message": f"Event '{event_name}' injected into simulation!", "severity": severity, "triggered_by": user.get('sub')}
    except Exception as e:
        logger.error(f"Failed to trigger event: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger event")

from app.services.feature_store import FeatureStore
from app.algorithms.models.lstm_predictor import LSTMPredictionEngine
from app.services.cache import redis_cache

feature_store = FeatureStore()
lstm_engine = LSTMPredictionEngine()

@router.get("/forecasts/risk", tags=["Dashboard"])
async def get_risk_forecast(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns AI forecasting outputs using the ML Prediction Layer and Feature Store.
    """
    # 1. Check Cache
    cache_key = "forecast_risk_usa"
    cached = await redis_cache.get(cache_key)
    if cached:
        return cached

    sim_state = getattr(request.app.state, "sim_state", None)
    if not sim_state:
        raise HTTPException(status_code=503, detail="Simulation not ready")

    try:
        # 1. Fetch ML Features from Database (Feature Store)
        seq = await feature_store.get_macro_sequence(country_code="USA")
        
        # 2. Run Inference using LSTM Model
        prediction = lstm_engine.predict(seq)
        
        # 3. Augment with active geopolitical risk from simulation
        crash_prob = 0.874 if sim_state.active_events else 0.125
        conflict_risk = 0.95 if any("War" in e for e in sim_state.active_events) else 0.241
        
        result = {
            "predicted_gdp_growth": prediction["predicted_gdp_growth"],
            "predicted_inflation": prediction["predicted_inflation"],
            "market_crash_probability": crash_prob,
            "conflict_risk": conflict_risk,
            "sentiment": "Markets panicked!" if sim_state.active_events else "Markets stable."
        }
        
        # Cache for 60 seconds
        await redis_cache.set(cache_key, result, ttl_seconds=60)
        
        return result
    except Exception as e:
        logger.error(f"Failed to generate risk forecast: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate risk forecast")

@router.get("/news", tags=["Dashboard"])
async def get_latest_news(request: Request, api_key: str = Depends(get_api_key)):
    """
    Returns AI-generated breaking news based on the real-time simulation state.
    """
    sim_state = getattr(request.app.state, "sim_state", None)
    if not sim_state:
        raise HTTPException(status_code=503, detail="Simulation not ready")
    
    state_dict = {
        "gdp_growth": 0.05 if sim_state.latest_global_state.get("total_gdp", 0) > 1200 else -0.05,
        "total_infected": sim_state.latest_global_state.get("total_infected", 0),
        "active_events": sim_state.active_events
    }
    
    try:
        headlines = news_gen.generate_news(state_dict)
        return {"headlines": headlines}
    except Exception as e:
        logger.error(f"Failed to generate news: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate news")

