import os
import sys
import pytest
import asyncio
from httpx import AsyncClient
from backend.app.main import app  # или из backend импортируй правильно, теперь PYTHONPATH = /app/backend

BASE_URL = "http://api:8000"

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        yield client