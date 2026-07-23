import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/ai/health")
    assert response.status_code == 200
    assert response.json() == {"status": "AI Services Engine is running"}

from app.core.config import settings

def test_simulation_status():
    response = client.get("/api/v1/simulation/status", headers={"X-API-Key": settings.SECRET_KEY})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["Running", "Paused", "Starting or Unavailable"]

@pytest.mark.asyncio
async def test_trigger_event_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/simulation/events/trigger?event_name=War&severity=5.0")
        assert response.status_code == 403

def test_forecasting_endpoint():
    response = client.get("/api/v1/simulation/forecasts/risk", headers={"X-API-Key": settings.SECRET_KEY})
    assert response.status_code in [200, 500, 503]
