"""Tests for RF Region API."""

import pytest
from async_test_client import AsyncTestClient

from machineq.core.rf_region.api import AsyncRFRegions


@pytest.fixture
def rf_regions_api(client: AsyncTestClient) -> AsyncRFRegions:
    """Get RF regions API resource from whichever client was requested."""
    return client.rf_regions


@pytest.mark.asyncio
class TestRFRegions:
    """RF Region API tests."""

    async def test_get_all(self, rf_regions_api: AsyncRFRegions):
        """Test listing all RF regions. Currently always returning an empty list"""
        await rf_regions_api.get_all()
