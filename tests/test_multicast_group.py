"""Tests for Multicast Group API."""

import pytest
from async_test_client import AsyncTestClient

from machineq import AsyncClient
from machineq.core.gateway import Coordinates, GatewayCreate
from machineq.core.multicast_group import (
    CreateMulticastGroupRequest,
    UpdateMulticastGroupRequest,
)
from machineq.core.multicast_group.api import AsyncMulticastGroups
from machineq.core.multicast_group.models import MulticastGroupType
from tests.sample_data.common import random_deveui, random_gateway_id, random_mac_address, random_name


@pytest.fixture
def multicast_groups_api(client: AsyncTestClient) -> AsyncMulticastGroups:
    """Get multicast groups API resource from whichever client was requested."""
    return client.multicast_groups


@pytest.mark.asyncio
class TestMulticastGroups:
    """Multicast Group API tests."""

    async def test_get_all(self, multicast_groups_api: AsyncMulticastGroups):
        """Test listing all multicast groups."""
        await multicast_groups_api.get_all()

    async def test_create_delete(self, multicast_groups_api: AsyncMulticastGroups):
        """Test creating and deleting a multicast group."""
        # Create a new multicast group
        deveui = random_deveui()  # Use last 8 characters of deveui for devaddr
        new_group = CreateMulticastGroupRequest(
            name=random_name(),
            multicast_deveui=deveui,
            multicast_dev_addr=deveui[-8:],
            multicast_app_s_key=deveui * 2,
            multicast_nwk_s_key=deveui * 2,
            group_type=MulticastGroupType.CLASS_C,
            data_rate=11,
            frequency=902300000,
        )
        created = await multicast_groups_api.create(new_group)
        try:
            assert created

            # test get and get_all
            group = await multicast_groups_api.get(deveui)
            assert group.multicast_deveui == deveui
            assert group.name == new_group.name
            assert group.multicast_dev_addr == new_group.multicast_dev_addr
            assert group.group_type == new_group.group_type
            assert group.data_rate == new_group.data_rate
            assert group.frequency == new_group.frequency
            all_groups = await multicast_groups_api.get_all()
            assert any(g.multicast_deveui == deveui for g in all_groups)
        finally:
            # Cleanup in case the delete failed
            if created:
                await multicast_groups_api.delete(deveui)

    async def test_update_patch(self, client: AsyncClient, multicast_groups_api: AsyncMulticastGroups):
        """Test that we can update and patch the Multicast group. Also, verify
        we can add devices and tag gateways"""
        deveui = random_deveui()
        new_group = CreateMulticastGroupRequest(
            name=random_name(),
            multicast_deveui=deveui,
            multicast_dev_addr=deveui[-8:],
            multicast_app_s_key=deveui * 2,
            multicast_nwk_s_key=deveui * 2,
            group_type=MulticastGroupType.CLASS_C,
            data_rate=11,
            frequency=902300000,
        )
        created = await multicast_groups_api.create(new_group)
        assert created
        gateway_id = ""
        try:
            update_data = UpdateMulticastGroupRequest(name=random_name(), data_rate=10, frequency=905200000)
            updated = await multicast_groups_api.update(deveui, update_data)
            assert updated
            # do a get and check that's true
            fetched = await multicast_groups_api.get(deveui)
            assert fetched.name == update_data.name
            assert fetched.data_rate == update_data.data_rate
            assert fetched.frequency == update_data.frequency
            # the group shouldn't have any gateways associated with it at first
            group_gateways = await multicast_groups_api.get_all_gateways(deveui)
            assert len(group_gateways) == 0
            # create a gateway and add it to the group
            node_id = random_gateway_id()
            profiles = await client.gateway_profiles.get_all()
            assert len(profiles) > 0, "No gateway profiles available for testing"
            gateway = GatewayCreate(
                node_id=node_id,
                name=random_name(),
                gateway_profile=profiles[0].id,
                mac_address=random_mac_address(),
                coordinates=Coordinates(
                    X="37.7749",
                    Y="-122.4194",
                ),
            )
            gateway_id = await client.gateways.create(gateway)
            # add the gateway to the group and ensure it was added
            add_result = await multicast_groups_api.add_gateways(deveui, [node_id])
            assert add_result.gateways_added == [node_id]
            assert len(add_result.gateways_ignored) == 0

            # try to add the same gateay again, and it should be ignored
            add_result = await multicast_groups_api.add_gateways(deveui, [node_id])
            assert add_result.gateways_ignored == [node_id]
            assert len(add_result.gateways_added) == 0

            # get the gateways and ensure the gateway is there
            fetched_gateways = await multicast_groups_api.get_all_gateways(deveui)
            assert fetched_gateways == [node_id]

            # now remove the gateway
            result = await multicast_groups_api.remove_gateways(deveui, [node_id])
            assert result.gateways_removed == [node_id]
            assert result.gateways_ignored == []

            # try removing again, would lead to gateway being ignored
            result = await multicast_groups_api.remove_gateways(deveui, [node_id])
            assert result.gateways_ignored == [node_id]
            assert result.gateways_removed == []

            # the gateway should be removed
            fetched_gateways = await multicast_groups_api.get_all_gateways(deveui)
            assert fetched_gateways == []
        finally:
            await multicast_groups_api.delete(deveui)
            if gateway_id:
                await client.gateways.delete(gateway_id)
