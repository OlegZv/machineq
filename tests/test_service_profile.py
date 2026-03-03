"""Tests for Service Profile API."""

import pytest

from machineq.core.service_profile.api import AsyncServiceProfiles, SyncServiceProfiles


@pytest.fixture
def service_profiles_api(client) -> SyncServiceProfiles | AsyncServiceProfiles:
    """Get service profiles API resource from whichever client was requested."""
    return client.service_profiles


@pytest.mark.asyncio
class TestServiceProfiles:
    """Service Profile API tests."""

    async def test_get_all(self, service_profiles_api):
        """Test listing all service profiles."""
        result = await service_profiles_api.get_all()
        assert len(result) > 0
