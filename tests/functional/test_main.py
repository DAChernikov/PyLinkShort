from httpx import AsyncClient
import pytest
from app.main import app

@pytest.mark.asyncio
async def test_startup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/docs")
        assert response.status_code == 200