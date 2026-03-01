"""Tests for Device Profile API."""

import pytest
from sample_data.common import random_deveui, random_name

from machineq.client.sync import SyncClient
from machineq.core.device.models import (
    ActivationType,
    DeviceCreate,
)
from machineq.core.device_profile.api import SyncDeviceProfiles
from machineq.core.device_profile.models import DeviceProfileDevicesUpdate


@pytest.fixture
def device_profiles_api(sync_client: SyncClient) -> SyncDeviceProfiles:
    """Get device profiles API resource."""
    return sync_client.device_profiles


class TestDeviceProfiles:
    """Device Profile API tests."""

    def test_get_all(self, device_profiles_api: SyncDeviceProfiles):
        """Test listing all device profiles."""
        result = device_profiles_api.get_all()
        assert len(result) > 0

    def test_device_profiles_update_devices(
        self,
        device_profiles_api: SyncDeviceProfiles,
        sync_client: SyncClient,
        get_service_profile,
        get_device_profile,
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

        created = sync_client.devices.create(device_data)
        try:
            # pick a different profile; skip if none available
            new_profile = get_device_profile(exclude=[original_profile])

            update = DeviceProfileDevicesUpdate(devices=[created])
            resp = device_profiles_api.update_devices(new_profile, update)
            assert len(resp.responses) == 1
            assert resp.responses[0].deveui == deveui
            assert resp.responses[0].response
            assert resp.responses[0].error == ""

            # verify
            fetched = sync_client.devices.get(created)
            assert fetched.deveui == deveui
            assert fetched.device_profile == new_profile
        finally:
            sync_client.devices.delete(created)
