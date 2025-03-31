import pytest
import httpx

@pytest.mark.asyncio
async def test_register_and_login():
    async with httpx.AsyncClient(base_url="http://api:8000") as client:
        await client.post("/api/auth/register", json={
            "username": "testuser1",
            "password": "secretpass",
            "email": "test@example.com"
        })
        res = await client.post("/api/auth/login", json={
            "username": "testuser1",
            "password": "secretpass"
        })
        assert res.status_code == 200
