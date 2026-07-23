from fastapi import APIRouter, Depends, HTTPException, Security, status, Request, WebSocket, WebSocketDisconnect
from fastapi.security.api_key import APIKeyHeader
import logging
from typing import Dict, Any
import json
import torch

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings
from app.ai.nlp.news_generator import NLPNewsGenerator
from app.domains.economy.finance.lstm_predictor import MarketLSTM

router = APIRouter()
logger = logging.getLogger("API_Simulation")
news_gen = NLPNewsGenerator()
limiter = Limiter(key_func=get_remote_address)

# Pre-load ML Model
lstm_model = MarketLSTM()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.SECRET_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

# --- WebSocket Connection Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, list] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
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
    engine = getattr(request.app.state, "engine", None)
    if not engine:
        return {"status": "Starting or Unavailable"}
        
    state = await engine.state_store.get_all()
    
    return {
        "tick": state.get("current_tick", 0),
        "status": "Running" if request.app.state.is_running else "Paused",
        "global_gdp": float(state.get("total_gdp", 0) / 1000),
        "co2_ppm": float(state.get("total_co2", 0) / 195),
        "active_events": state.get("active_crises", [])
    }

from app.core.security import require_role

@router.post("/events/trigger", tags=["Control Panel"])
@limiter.limit("5/minute")
async def trigger_event(
    request: Request, 
    event_name: str, 
    severity: float, 
    api_key: str = Depends(get_api_key),
    user: Dict = Depends(require_role("admin"))
):
    if not (1.0 <= severity <= 10.0):
        raise HTTPException(status_code=400, detail="Severity must be between 1.0 and 10.0")

    engine = getattr(request.app.state, "engine", None)
    if not engine:
        raise HTTPException(status_code=503, detail="Simulation not ready")
        
    try:
        # Push event directly into the global state store so all domains can react
        current_crises = await engine.state_store.get("active_crises", [])
        current_crises.append({"name": event_name, "severity": severity})
        await engine.state_store.set("active_crises", current_crises)
        
        logger.info(f"Triggered real event {event_name} via API by user {user.get('sub')}")
        return {"message": f"Event '{event_name}' injected into simulation!", "severity": severity, "triggered_by": user.get('sub')}
    except Exception as e:
        logger.error(f"Failed to trigger event: {e}")
        raise HTTPException(status_code=500, detail="Failed to trigger event")


from app.services.cache import redis_cache

@router.get("/forecasts/risk", tags=["Dashboard"])
async def get_risk_forecast(request: Request, api_key: str = Depends(get_api_key)):
    cache_key = "forecast_risk_global"
    cached = await redis_cache.get(cache_key)
    if cached:
        return cached

    engine = getattr(request.app.state, "engine", None)
    if not engine:
        raise HTTPException(status_code=503, detail="Simulation not ready")

    try:
        state = await engine.state_store.get_all()
        crises = state.get("active_crises", [])
        
        # 1. Provide mock feature tensor to LSTM (in reality this comes from FeatureStore)
        mock_features = torch.randn(1, 10, 5)
        
        # 2. Run Inference using new MarketLSTM
        prediction_tensor = lstm_model.predict(mock_features)
        predicted_growth = prediction_tensor.item()
        
        crash_prob = 0.874 if crises else 0.125
        
        result = {
            "predicted_gdp_growth": predicted_growth,
            "market_crash_probability": crash_prob,
            "sentiment": "Markets panicked!" if crises else "Markets stable."
        }
        
        await redis_cache.set(cache_key, result, ttl_seconds=10)
        
        return result
    except Exception as e:
        logger.error(f"Failed to generate risk forecast: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate risk forecast")

@router.get("/news", tags=["Dashboard"])
async def get_latest_news(request: Request, api_key: str = Depends(get_api_key)):
    engine = getattr(request.app.state, "engine", None)
    if not engine:
        raise HTTPException(status_code=503, detail="Simulation not ready")
    
    state = await engine.state_store.get_all()
    
    state_dict = {
        "gdp_growth": 0.05 if state.get("total_gdp", 0) > 1200 else -0.05,
        "total_infected": state.get("total_infected", 0),
        "active_events": [c["name"] for c in state.get("active_crises", [])]
    }
    
    try:
        headlines = news_gen.generate_news(state_dict)
        return {"headlines": headlines}
    except Exception as e:
        logger.error(f"Failed to generate news: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate news")

@router.get("/insights", tags=["Dashboard"])
async def get_ai_insights(request: Request, api_key: str = Depends(get_api_key)):
    # Generate some dynamic mock insights for the dashboard
    import random
    
    # Check if there are active crises
    engine = getattr(request.app.state, "engine", None)
    active_crises = []
    if engine:
        state = await engine.state_store.get_all()
        active_crises = state.get("active_crises", [])
        
    base_insights = [
        {"t": "Agent 14 detected regime shift in copper futures", "c": "Macro Agent"},
        {"t": "New satellite data ingested (Sentinel-2)", "c": "Data Pipeline"},
        {"t": "Ensemble retrained — accuracy +0.4pp", "c": "ML Ops"},
        {"t": "Treasury auction outlier flagged", "c": "Macro Agent"},
        {"t": "EUR/USD ensemble diverging — increased volatility expected", "c": "FX Agent"},
        {"t": "Taiwan strait tension index up 18% w/w — review supply chain B17", "c": "Geo Agent"},
        {"t": "Brent crude likely to test $112 within 21 days (P=0.74)", "c": "Macro Agent"}
    ]
    
    # Shuffle and pick 3-4 insights
    random.shuffle(base_insights)
    num_insights = random.randint(3, 4)
    selected_insights = base_insights[:num_insights]
    
    if active_crises:
        crisis = active_crises[-1]
        selected_insights.insert(0, {
            "t": f"Emergency Response Agent activated for {crisis['name']}",
            "c": "Geo Agent"
        })
        
    return {"insights": selected_insights[:4]}

@router.get("/alerts", tags=["Dashboard"])
async def get_risk_alerts(request: Request, api_key: str = Depends(get_api_key)):
    import random
    
    engine = getattr(request.app.state, "engine", None)
    if not engine:
        raise HTTPException(status_code=503, detail="Simulation not ready")
        
    state = await engine.state_store.get_all()
    active_crises = state.get("active_crises", [])
    
    alerts = []
    
    # Add real active crises from the simulation state
    for crisis in active_crises:
        tone = "danger" if crisis["severity"] > 7.0 else "warning"
        alerts.append({"title": crisis["name"], "tone": tone})
        
    # Add some mock ambient alerts if there are none, to populate the UI
    if len(alerts) < 3:
        ambient_alerts = [
            {"title": "Red Sea shipping disruption", "tone": "danger"},
            {"title": "Argentina sovereign downgrade", "tone": "warning"},
            {"title": "Pacific cyclone formation", "tone": "warning"},
            {"title": "Unusual options activity in energy sector", "tone": "warning"}
        ]
        random.shuffle(ambient_alerts)
        alerts.extend(ambient_alerts[:3 - len(alerts)])
        
    return {"alerts": alerts[:3]}

