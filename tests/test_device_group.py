"""Tests for Device Group API."""

import pytest
from sample_data.common import random_deveui, random_name

from machineq.core.device import DeviceCreate
from machineq.core.device.models import ActivationType
from machineq.core.device_group.api import AsyncDeviceGroups, SyncDeviceGroups
from machineq.core.device_group.models import DeviceGroupCreate, DeviceGroupPatch, DeviceGroupUpdate


@pytest.fixture
def device_groups_api(client) -> SyncDeviceGroups | AsyncDeviceGroups:
    """Get device groups API resource."""
    return client.device_groups


@pytest.mark.asyncio
class TestDeviceGroups:
    """Device Group API tests."""

    async def test_get_all(self, device_groups_api):
        """Test listing all device groups."""
        _groups = await device_groups_api.get_all()

    async def test_create_and_delete(self, device_groups_api):
        """Test creating and deleting a device group."""
        data = DeviceGroupCreate(name=random_name(), device_list=[])
        group_id = await device_groups_api.create(data)

        try:
            group = await device_groups_api.get(group_id)
            assert group.id == group_id
            # get all should contain the created group too
            all_groups = await device_groups_api.get_all()
            assert any(g.id == group_id for g in all_groups)
        finally:
            await device_groups_api.delete(group_id)

    async def test_device_groups_update_and_patch(
        self,
        device_groups_api,
        get_service_profile,
        get_device_profile,
    ):
        """Test updating and patching a device group."""
        data = DeviceGroupCreate(name=random_name(), device_list=[])
        group_id = await device_groups_api.create(data)
        device_id = ""
        try:
            # create new devices to associate to the group
            deveui = random_deveui()
            service_profile = get_service_profile()
            device_profile = get_device_profile()
            device_data = DeviceCreate(
                name=deveui,
                deveui=deveui,
                activation_type=ActivationType.OTAA,
                service_profile=service_profile,
                device_profile=device_profile,
                application_eui=deveui,
                application_key=deveui * 2,
            )
            device_id = await device_groups_api.client.devices.create(device_data)
            assert device_id

            update_data = DeviceGroupUpdate(name=random_name(), device_list=[device_id])
            updated = await device_groups_api.update(group_id, update_data)
            assert updated

            # verify
            fetched = await device_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert fetched.device_list == [device_id]
            assert len(fetched.devices) == 1
            assert fetched.devices[0].deveui == device_id

            # for the patch just remove the devices, and keep the name unchanged
            patch_data = DeviceGroupPatch(device_list=[""])
            patched = await device_groups_api.patch(group_id, patch_data)

            assert patched

            fetched = await device_groups_api.get(group_id)
            assert fetched.id == group_id
            assert fetched.name == update_data.name
            assert fetched.device_list == [""]
            assert fetched.devices == []

        finally:
            await device_groups_api.delete(group_id)
            if device_id:
                await device_groups_api.client.devices.delete(device_id)
