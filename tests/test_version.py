"""Tests for Version API."""

import pytest
from async_test_client import AsyncTestClient

from machineq.core.version.api import AsyncVersion


@pytest.fixture
def version_api(client: AsyncTestClient) -> AsyncVersion:
    """Get version API resource from whichever client was requested."""
    return client.version


@pytest.mark.asyncio
class TestVersion:
    """Version API tests."""

    async def test_get(self, version_api: AsyncVersion):
        """Test getting API version information."""
        await version_api.get()
