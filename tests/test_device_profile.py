"""Tests for Device Profile API."""

import pytest
from async_test_client import AsyncTestClient
from conftest import ProfileGetter
from sample_data.common import random_deveui, random_name

from machineq.core.device.models import (
    ActivationType,
    DeviceCreate,
)
from machineq.core.device_profile.api import AsyncDeviceProfiles
from machineq.core.device_profile.models import DeviceProfileDevicesUpdate


@pytest.fixture
def device_profiles_api(client: AsyncTestClient) -> AsyncDeviceProfiles:
    """Get device profiles API resource from whatever client was requested."""
    # client is already wrapped so simply accessing the attribute is safe
    return client.device_profiles


@pytest.mark.asyncio
class TestDeviceProfiles:
    """Device Profile API tests."""

    async def test_get_all(self, device_profiles_api: AsyncDeviceProfiles):
        """Test listing all device profiles."""
        result = await device_profiles_api.get_all()
        assert len(result) > 0

    async def test_device_profiles_update_devices(
        self,
        device_profiles_api: AsyncDeviceProfiles,
        client: AsyncTestClient,
        get_service_profile: ProfileGetter,
        get_device_profile: ProfileGetter,
    ):
        """Test updating devices for a device profile (patch devices association)."""
        # create a device to associate
        deveui = random_deveui()
        original_profile = get_device_profile()
        device_data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=get_service_profile(),
            device_profile=original_profile,
            application_eui=deveui,
            application_key=deveui * 2,
        )

        created = await client.devices.create(device_data)
        try:
            # pick a different profile; skip if none available
            new_profile = get_device_profile(exclude=[original_profile])

            update = DeviceProfileDevicesUpdate(devices=[created])
            resp = await device_profiles_api.update_devices(new_profile, update)
            assert len(resp.responses) == 1
            assert resp.responses[0].deveui == deveui
            assert resp.responses[0].response
            assert resp.responses[0].error == ""

            # verify
            fetched = await client.devices.get(created)
            assert fetched.deveui == deveui
            assert fetched.device_profile == new_profile
        finally:
            await client.devices.delete(created)
