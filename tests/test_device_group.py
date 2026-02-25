"""Tests for Device Group API."""

import pytest
from sample_data.common import random_name

from machineq.client.sync import SyncClient
from machineq.core.device_group.api import SyncDeviceGroups
from machineq.core.device_group.models import DeviceGroupCreate


@pytest.fixture
def device_groups_api(sync_client: SyncClient) -> SyncDeviceGroups:
    """Get device groups API resource."""
    return sync_client.device_groups


class TestDeviceGroups:
    """Device Group API tests."""

    def test_get_all(self, device_groups_api: SyncDeviceGroups):
        """Test listing all device groups."""
        device_groups_api.get_all()

    def test_create_and_delete(self, device_groups_api: SyncDeviceGroups):
        """Test creating and deleting a device group."""
        data = DeviceGroupCreate(name=random_name(), device_list=[])
        group_id = device_groups_api.create(data)

        try:
            group = device_groups_api.get(group_id)
            assert group.id == group_id
        finally:
            device_groups_api.delete(group_id)
