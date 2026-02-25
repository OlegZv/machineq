"""Tests for Gateway API."""

import pytest
from sample_data.common import random_gateway_id, random_mac_address, random_name

from machineq.client.sync import SyncClient
from machineq.core.gateway import Coordinates
from machineq.core.gateway.api import SyncGateways
from machineq.core.gateway.models import GatewayCreate


@pytest.fixture
def gateways_api(sync_client: SyncClient) -> SyncGateways:
    """Get gateways API resource."""
    return sync_client.gateways


class TestGateways:
    """Gateway API tests."""

    def test_get_all(self, gateways_api: SyncGateways):
        """Test listing all gateways."""
        gateways_api.get_all()

    def test_get_existing_gateway(self, gateways_api: SyncGateways):
        """Test retrieving a specific gateway."""
        gateways = gateways_api.get_all()
        if gateways:
            gateway_id = gateways[0].id
            result = gateways_api.get(gateway_id)
            assert result.id == gateway_id

    def test_create_and_delete(self, gateways_api: SyncGateways):
        """Test creating and deleting a gateway."""
        gateway_id = random_gateway_id()
        data = GatewayCreate(
            node_id=gateway_id,
            name=random_name(),
            gateway_profile=self.get_gateway_profile(gateways_api.client),
            mac_address=random_mac_address(),
            coordinates=Coordinates(
                X="37.7749",
                Y="-122.4194",
            ),
        )

        created_id = gateways_api.create(data)

        try:
            gateway = gateways_api.get(created_id)
            assert gateway.id == created_id
        finally:
            gateways_api.delete(created_id)

    def test_get_statistics(self, gateways_api: SyncGateways):
        """Test getting gateway statistics."""
        gateways = gateways_api.get_all()
        if gateways:
            gateway_id = gateways[0].id
            gateways_api.get_statistics(gateway_id)

    def get_gateway_profile(self, client: SyncClient) -> str:
        """Helper to get a gateway profile ID."""
        profiles = client.gateway_profiles.get_all()
        assert len(profiles) > 0, "No gateway profiles available for testing"
        return profiles[0].id
