"""Tests for Gateway Group API."""

import pytest
from sample_data.common import random_name

from machineq.client.sync import SyncClient
from machineq.core.gateway_group.api import SyncGatewayGroups
from machineq.core.gateway_group.models import GatewayGroupCreate


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
