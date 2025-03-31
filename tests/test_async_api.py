import pytest
import httpx
import asyncio
import subprocess
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.main import app

BASE_URL = "http://api:8000"

@pytest.fixture(scope="session", autouse=True)
def start_server():
    proc = subprocess.Popen(["python", "backend/app/main.py"])
    time.sleep(2)  # даем серверу подняться
    yield
    proc.terminate()


@pytest.mark.asyncio
async def test_register_and_login():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Регистрация
        res = await client.post("/api/auth/register", json={
            "username": "testuser1",
            "password": "secretpass",
            "email": "test@example.com"
        })
        assert res.status_code in (201, 400)  # возможно пользователь уже есть

        # Логин
        res = await client.post("/api/auth/login", json={
            "username": "testuser1",
            "password": "secretpass"
        })
        assert res.status_code == 200
        session_id = res.cookies.get("session_id")
        assert session_id

        # Профиль
        res = await client.get("/api/auth/profile", cookies={"session_id": session_id})
        assert res.status_code == 200
        assert res.json()["username"] == "testuser1"