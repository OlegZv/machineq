"""Tests for RF Region API."""

import pytest

from machineq.core.rf_region.api import AsyncRFRegions, SyncRFRegions


@pytest.fixture
def rf_regions_api(client) -> SyncRFRegions | AsyncRFRegions:
    """Get RF regions API resource from whichever client was requested."""
    return client.rf_regions


@pytest.mark.asyncio
class TestRFRegions:
    """RF Region API tests."""

    async def test_get_all(self, rf_regions_api):
        """Test listing all RF regions. Currently always returning an empty list"""
        await rf_regions_api.get_all()
