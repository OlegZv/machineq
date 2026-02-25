"""Tests for Version API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.version.api import SyncVersion


@pytest.fixture
def version_api(sync_client: SyncClient) -> SyncVersion:
    """Get version API resource."""
    return sync_client.version


class TestVersion:
    """Version API tests."""

    def test_get(self, version_api: SyncVersion):
        """Test getting API version information."""
        version_api.get()
