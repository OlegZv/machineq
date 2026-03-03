"""Tests for Gateway API."""

import pytest
from sample_data.common import random_gateway_id, random_mac_address, random_name

from machineq.core.gateway import Coordinates
from machineq.core.gateway.api import AsyncGateways, SyncGateways
from machineq.core.gateway.models import GatewayCreate, GatewayPatch, GatewayUpdate, LocationType


@pytest.fixture
def gateways_api(client) -> SyncGateways | AsyncGateways:
    """Get gateways API resource from whichever client was requested."""
    return client.gateways


@pytest.mark.asyncio
class TestGateways:
    """Gateway API tests."""

    async def test_get_all(self, gateways_api):
        """Test listing all gateways."""
        await gateways_api.get_all()

    async def test_get_existing_gateway(self, gateways_api):
        """Test retrieving a specific gateway."""
        gateways = await gateways_api.get_all()
        if gateways:
            gateway_id = gateways[0].id
            result = await gateways_api.get(gateway_id)
            assert result.id == gateway_id

    async def test_create_and_delete(self, gateways_api):
        """Test creating and deleting a gateway."""
        gateway_id = random_gateway_id()
        data = GatewayCreate(
            node_id=gateway_id,
            name=random_name(),
            gateway_profile=await self.get_gateway_profile(gateways_api.client),
            mac_address=random_mac_address(),
            coordinates=Coordinates(
                X="37.7749",
                Y="-122.4194",
            ),
        )

        created_id = await gateways_api.create(data)

        try:
            gateway = await gateways_api.get(created_id)
            assert gateway.id == created_id
        finally:
            await gateways_api.delete(created_id)

    async def test_gateways_update_and_patch(self, gateways_api):
        """Test updating and patching a gateway by using the fetched instance to build update payload."""
        gateway_id = random_gateway_id()
        data = GatewayCreate(
            node_id=gateway_id,
            name=random_name(),
            gateway_profile=await self.get_gateway_profile(gateways_api.client),
            mac_address=random_mac_address(),
            coordinates=Coordinates(X="37.7749", Y="-122.4194"),
        )

        created_id = await gateways_api.create(data)

        try:
            gateway = await gateways_api.get(created_id)

            update_data = GatewayUpdate(
                name=random_name(),
                antenna_gain="1",
                location_type=LocationType.OUTDOOR,
                coordinates=Coordinates(X="0", Y="0"),
                gateway_profile=gateway.gateway_profile,
                cellular_enabled=True,
            )

            updated = await gateways_api.update(created_id, update_data)
            assert updated
            # check the updated gateway
            fetched = await gateways_api.get(created_id)
            assert fetched.id == created_id
            assert fetched.name == update_data.name
            assert fetched.antenna_gain == update_data.antenna_gain
            assert fetched.location_type == update_data.location_type
            assert fetched.coordinates == update_data.coordinates
            assert fetched.cellular_enabled == update_data.cellular_enabled

            patch_data = GatewayPatch(
                name=random_name(),
                coordinates=Coordinates(X="1", Y="1"),
            )
            patched = await gateways_api.patch(created_id, patch_data)

            assert patched

            fetched = await gateways_api.get(created_id)
            assert fetched.id == created_id
            assert fetched.name == patch_data.name
            assert fetched.coordinates == patch_data.coordinates
            # the fields not included in the patch should remain unchanged from the update
            assert fetched.antenna_gain == update_data.antenna_gain
            assert fetched.location_type == update_data.location_type
            assert fetched.cellular_enabled == update_data.cellular_enabled

        finally:
            await gateways_api.delete(created_id)

    async def test_get_statistics(self, gateways_api):
        """Test getting gateway statistics."""
        gateways = await gateways_api.get_all()
        if gateways:
            gateway_id = gateways[0].id
            await gateways_api.get_statistics(gateway_id)

    async def get_gateway_profile(self, client) -> str:
        """Helper to get a gateway profile ID."""
        profiles = await client.gateway_profiles.get_all()
        assert len(profiles) > 0, "No gateway profiles available for testing"
        return profiles[0].id
