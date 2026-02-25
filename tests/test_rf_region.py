"""Tests for RF Region API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.rf_region.api import SyncRFRegions


@pytest.fixture
def rf_regions_api(sync_client: SyncClient) -> SyncRFRegions:
    """Get RF regions API resource."""
    return sync_client.rf_regions


class TestRFRegions:
    """RF Region API tests."""

    def test_get_all(self, rf_regions_api: SyncRFRegions):
        """Test listing all RF regions. Currently always returning an empty list"""
        rf_regions_api.get_all()
