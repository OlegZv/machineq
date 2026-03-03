"""Tests for Gateway Profile API."""

import pytest

from machineq.core.gateway_profile.api import AsyncGatewayProfiles, SyncGatewayProfiles


@pytest.fixture
def gateway_profiles_api(client) -> SyncGatewayProfiles | AsyncGatewayProfiles:
    """Get gateway profiles API resource."""
    return client.gateway_profiles


@pytest.mark.asyncio
class TestGatewayProfiles:
    """Gateway Profile API tests."""

    async def test_get_all(self, gateway_profiles_api):
        """Test listing all gateway profiles."""
        result = await gateway_profiles_api.get_all()
        assert len(result) > 0
