import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}