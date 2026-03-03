"""Tests for Version API."""

import pytest

from machineq.core.version.api import AsyncVersion, SyncVersion


@pytest.fixture
def version_api(client) -> SyncVersion | AsyncVersion:
    """Get version API resource from whichever client was requested."""
    return client.version


@pytest.mark.asyncio
class TestVersion:
    """Version API tests."""

    async def test_get(self, version_api):
        """Test getting API version information."""
        await version_api.get()
