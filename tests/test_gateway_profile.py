"""Tests for Gateway Profile API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.gateway_profile.api import SyncGatewayProfiles


@pytest.fixture
def gateway_profiles_api(sync_client: SyncClient) -> SyncGatewayProfiles:
    """Get gateway profiles API resource."""
    return sync_client.gateway_profiles


class TestGatewayProfiles:
    """Gateway Profile API tests."""

    def test_get_all(self, gateway_profiles_api: SyncGatewayProfiles):
        """Test listing all gateway profiles."""
        result = gateway_profiles_api.get_all()
        assert len(result) > 0
