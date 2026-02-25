"""Tests for Service Profile API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.service_profile.api import SyncServiceProfiles


@pytest.fixture
def service_profiles_api(sync_client: SyncClient) -> SyncServiceProfiles:
    """Get service profiles API resource."""
    return sync_client.service_profiles


class TestServiceProfiles:
    """Service Profile API tests."""

    def test_get_all(self, service_profiles_api: SyncServiceProfiles):
        """Test listing all service profiles."""
        result = service_profiles_api.get_all()
        assert len(result) > 0
