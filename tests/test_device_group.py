"""Tests for Device Group API."""

import pytest
from sample_data.common import random_deveui, random_name

from machineq.client.sync import SyncClient
from machineq.core.device import DeviceCreate
from machineq.core.device.models import ActivationType
from machineq.core.device_group.api import SyncDeviceGroups
from machineq.core.device_group.models import DeviceGroupCreate, DeviceGroupPatch, DeviceGroupUpdate


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

    def test_device_groups_update_and_patch(self, device_groups_api: SyncDeviceGroups):
        """Test updating and patching a device group."""
        data = DeviceGroupCreate(name=random_name(), device_list=[])
        group_id = device_groups_api.create(data)
        device_id = ""
        try:
            # create new devices to associate to the group
            deveui = random_deveui()
            service_profiles = device_groups_api.client.service_profiles.get_all()
            device_profiles = device_groups_api.client.device_profiles.get_all()
            assert len(service_profiles) > 0
            assert len(device_profiles) > 0
            device_data = DeviceCreate(
                name=deveui,
                deveui=deveui,
                activation_type=ActivationType.OTAA,
                service_profile=service_profiles[0].id,
                device_profile=device_profiles[0].id,
                application_eui=deveui,
                application_key=deveui * 2,
            )
            device_id = device_groups_api.client.devices.create(device_data)
            assert device_id

            update_data = DeviceGroupUpdate(name=random_name(), device_list=[device_id])
            updated = device_groups_api.update(group_id, update_data)
            assert updated

            # verify
            fetched = device_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert fetched.device_list == [device_id]
            assert len(fetched.devices) == 1
            assert fetched.devices[0].deveui == device_id

            # for the patch just remove the devices, and keep the name unchanged
            patch_data = DeviceGroupPatch(device_list=[""])
            patched = device_groups_api.patch(group_id, patch_data)

            assert patched

            fetched = device_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert fetched.device_list == [""]
            assert fetched.devices == []

        finally:
            device_groups_api.delete(group_id)
            if device_id:
                device_groups_api.client.devices.delete(device_id)
