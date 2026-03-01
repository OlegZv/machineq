"""Tests for Gateway Group API."""

import pytest
from sample_data.common import random_gateway_id, random_mac_address, random_name

from machineq.client.sync import SyncClient
from machineq.core.gateway import Coordinates, GatewayCreate
from machineq.core.gateway_group.api import SyncGatewayGroups
from machineq.core.gateway_group.models import GatewayGroupCreate, GatewayGroupPatch, GatewayGroupUpdate


@pytest.fixture
def gateway_groups_api(sync_client: SyncClient) -> SyncGatewayGroups:
    """Get gateway groups API resource."""
    return sync_client.gateway_groups


class TestGatewayGroups:
    """Gateway Group API tests."""

    def test_get_all(self, gateway_groups_api: SyncGatewayGroups):
        """Test listing all gateway groups."""
        gateway_groups_api.get_all()

    def test_create_and_delete(self, gateway_groups_api: SyncGatewayGroups):
        """Test creating and deleting a gateway group."""
        data = GatewayGroupCreate(name=random_name(), gateway_list=[])
        group_id = gateway_groups_api.create(data)

        try:
            group = gateway_groups_api.get(group_id)
            assert group.id == group_id
        finally:
            gateway_groups_api.delete(group_id)

    def test_gateway_groups_update_and_patch(self, gateway_groups_api: SyncGatewayGroups):
        """Test updating and patching a gateway group."""
        data = GatewayGroupCreate(name=random_name(), gateway_list=[])
        group_id = gateway_groups_api.create(data)
        new_gw_id = ""

        try:
            # create new gateway to add to the group
            gw_profiles = gateway_groups_api.client.gateway_profiles.get_all()
            assert len(gw_profiles) > 0

            gw_data = GatewayCreate(
                node_id=random_gateway_id(),
                name=random_name(),
                gateway_profile=gw_profiles[0].id,
                mac_address=random_mac_address(),
                coordinates=Coordinates(X="0", Y="0"),
            )
            new_gw_id = gateway_groups_api.client.gateways.create(gw_data)
            assert new_gw_id
            group = gateway_groups_api.get(group_id)
            assert group.name == data.name
            assert group.gateway_list == [""]
            assert group.gateways == []

            update_data = GatewayGroupUpdate(name=random_name(), gateway_list=[new_gw_id])
            updated = gateway_groups_api.update(group_id, update_data)
            assert updated

            # verify
            fetched = gateway_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert len(fetched.gateway_list) == 1
            assert fetched.gateway_list[0] == new_gw_id
            assert len(fetched.gateways) == 1
            assert fetched.gateways[0].id == new_gw_id

            # in the patch, just remove gateways from the group and keep the name unchanged
            patch_data = GatewayGroupPatch(gateway_list=[""])
            patched = gateway_groups_api.patch(group_id, patch_data)

            assert patched

            fetched = gateway_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert fetched.gateway_list == [""]
            assert fetched.gateways == []

        finally:
            gateway_groups_api.delete(group_id)
            if new_gw_id:
                gateway_groups_api.client.gateways.delete(new_gw_id)
