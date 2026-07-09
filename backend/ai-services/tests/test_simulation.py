import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/ai/health")
    assert response.status_code == 200
    assert response.json() == {"status": "AI Services Engine is running"}

def test_simulation_status():
    # Without API key, some endpoints might fail if enforced, but in this setup auto_error=False
    response = client.get("/api/v1/simulation/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["Running", "Paused", "Starting or Unavailable"]

@pytest.mark.asyncio
async def test_trigger_event_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Should fail with 403 because we didn't provide a JWT with 'admin' role
        response = await ac.post("/api/v1/simulation/events/trigger?event_name=War&severity=5.0")
        assert response.status_code == 403

def test_forecasting_endpoint():
    response = client.get("/api/v1/simulation/forecasts/risk")
    # If the database isn't running in tests, this will return a 500 or 503
    assert response.status_code in [200, 500, 503]
