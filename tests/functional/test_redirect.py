import pytest
import httpx

@pytest.mark.asyncio
async def test_redirect_unknown():
    async with httpx.AsyncClient(base_url="http://api:8000") as client:
        res = await client.get("/unknown")
        assert res.status_code == 404