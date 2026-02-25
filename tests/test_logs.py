"""Tests for Logs API."""

from datetime import datetime, timedelta

import pytest

from machineq.client.sync import SyncClient
from machineq.core.logs.api import SyncLogs


@pytest.fixture
def logs_api(sync_client: SyncClient) -> SyncLogs:
    """Get logs API resource."""
    return sync_client.logs


class TestLogs:
    """Logs API tests."""

    def test_get_all_no_filter(self, logs_api: SyncLogs):
        """Test getting logs without filters."""
        logs = logs_api.get_all()
        assert len(logs) > 0

    def test_get_all_with_device_filter(self, logs_api: SyncLogs, sync_client: SyncClient):
        """Test getting logs filtered by device EUI."""
        devices = sync_client.devices.get_all()
        if devices:
            deveui = devices[0].deveui
            logs_api.get_all(deveui=deveui)

    def test_get_all_time_filter(self, logs_api: SyncLogs):
        """Test getting logs without filters."""
        # timezone intentionally naive
        now = datetime.now()
        ten_hours_ago = now - timedelta(hours=10)
        with pytest.warns(UserWarning, match="Naive datetime provided.*"):
            logs = logs_api.get_all(start_time=ten_hours_ago, end_time=now)
            assert len(logs) > 0
