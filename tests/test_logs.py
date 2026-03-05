"""Tests for Logs API."""

from datetime import datetime, timedelta

import pytest
from async_test_client import AsyncTestClient

from machineq.core.logs.api import AsyncLogs


@pytest.fixture
def logs_api(client: AsyncTestClient) -> AsyncLogs:
    """Get logs API resource from whichever client was requested."""
    return client.logs


@pytest.mark.asyncio
class TestLogs:
    """Logs API tests."""

    async def test_get_all_no_filter(self, logs_api: AsyncLogs):
        """Test getting logs without filters."""
        logs = await logs_api.get_all()
        assert len(logs) > 0

    async def test_get_all_with_device_filter(self, logs_api: AsyncLogs, client: AsyncTestClient):
        """Test getting logs filtered by device EUI."""
        devices = await client.devices.get_all()
        if devices:
            deveui = devices[0].deveui
            await logs_api.get_all(deveui=deveui)

    async def test_get_all_time_filter(self, logs_api: AsyncLogs):
        """Test getting logs without filters."""
        # timezone intentionally naive
        now = datetime.now()
        ten_hours_ago = now - timedelta(hours=10)
        with pytest.warns(UserWarning, match="Naive datetime provided.*"):
            logs = await logs_api.get_all(start_time=ten_hours_ago, end_time=now)
            assert len(logs) > 0
