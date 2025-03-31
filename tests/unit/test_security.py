import pytest
from app.core.security import create_session, delete_session
from unittest.mock import patch
import uuid

@patch("app.core.security.redis_client")
def test_create_session(mock_redis):
    token = create_session(1)
    assert token.startswith(str(uuid.UUID(token)))  # валидный UUID
    mock_redis.setex.assert_called_once()

@patch("app.core.security.redis_client")
def test_delete_session(mock_redis):
    delete_session("abc")
    mock_redis.delete.assert_called_once_with("session:abc")
