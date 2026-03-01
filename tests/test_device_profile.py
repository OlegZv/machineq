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

    def test_device_profiles_update_devices(self, device_profiles_api: SyncDeviceProfiles, sync_client: SyncClient):
        """Test updating devices for a device profile (patch devices association)."""
        # create a device to associate
        deveui = random_deveui()
        service_profiles = sync_client.service_profiles.get_all()
        device_profiles = sync_client.device_profiles.get_all()
        assert len(service_profiles) > 0
        assert len(device_profiles) > 0
        original_profile = device_profiles[0].id
        device_data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=service_profiles[0].id,
            device_profile=original_profile,
            application_eui=deveui,
            application_key=deveui * 2,
        )

        created = sync_client.devices.create(device_data)
        try:
            profiles = device_profiles_api.get_all()
            assert len(profiles) > 1
            new_profile = next((p for p in profiles if p.id != original_profile), None)
            assert new_profile is not None

            update = DeviceProfileDevicesUpdate(devices=[created])
            resp = device_profiles_api.update_devices(new_profile.id, update)
            assert len(resp.responses) == 1
            assert resp.responses[0].deveui == deveui
            assert resp.responses[0].response
            assert resp.responses[0].error == ""

            # verify
            fetched = sync_client.devices.get(created)
            assert fetched.deveui == deveui
            assert fetched.device_profile == new_profile.id
        finally:
            sync_client.devices.delete(created)
