"""Tests for Multicast Group API."""

import pytest

from machineq.core.multicast_group.api import AsyncMulticastGroups, SyncMulticastGroups


@pytest.fixture
def multicast_groups_api(client) -> SyncMulticastGroups | AsyncMulticastGroups:
    """Get multicast groups API resource from whichever client was requested."""
    return client.multicast_groups


@pytest.mark.asyncio
class TestMulticastGroups:
    """Multicast Group API tests."""

    async def test_get_all(self, multicast_groups_api):
        """Test listing all multicast groups."""
        await multicast_groups_api.get_all()
