"""Tests for Device Profile API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.device_profile.api import SyncDeviceProfiles


@pytest.fixture
def device_profiles_api(sync_client: SyncClient) -> SyncDeviceProfiles:
    """Get device profiles API resource."""
    return sync_client.device_profiles


class TestDeviceProfiles:
    """Device Profile API tests."""

    def test_get_all(self, device_profiles_api: SyncDeviceProfiles):
        """Test listing all device profiles."""
        result = device_profiles_api.get_all()
        assert len(result) > 0
