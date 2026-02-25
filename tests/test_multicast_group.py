"""Tests for Multicast Group API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.multicast_group.api import SyncMulticastGroups


@pytest.fixture
def multicast_groups_api(sync_client: SyncClient) -> SyncMulticastGroups:
    """Get multicast groups API resource."""
    return sync_client.multicast_groups


class TestMulticastGroups:
    """Multicast Group API tests."""

    def test_get_all(self, multicast_groups_api: SyncMulticastGroups):
        """Test listing all multicast groups."""
        multicast_groups_api.get_all()
