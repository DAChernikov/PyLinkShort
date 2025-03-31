import asyncio
import pytest
from unittest.mock import patch, MagicMock

from app.services import analytics

@pytest.mark.asyncio
async def test_update_link_stats():
    mock_loop = MagicMock()
    future = asyncio.Future()
    future.set_result(None)
    mock_loop.run_in_executor.return_value = future

    with patch("app.services.analytics.asyncio.get_event_loop", return_value=mock_loop):
        await analytics.update_link_stats("testcode")

    mock_loop.run_in_executor.assert_called_once()
    args = mock_loop.run_in_executor.call_args[0]
    assert args[1].__name__ == "_update_link_stats"
    assert args[2] == "testcode"