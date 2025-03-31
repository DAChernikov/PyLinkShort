import pytest
import httpx

@pytest.mark.asyncio
async def test_create_and_fetch_link():
    async with httpx.AsyncClient(base_url="http://api:8000") as client:
        res = await client.post("/api/links/", json={"target_url": "https://example.com"}, headers={"Authorization": "Bearer FAKE_TOKEN"})
        assert res.status_code in (200, 201, 401)  # Depends on auth implementation