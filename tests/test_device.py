"""Tests for Device API."""

import pytest
from sample_data.common import (
    random_deveui,
    random_hex,
    random_name,
)

from machineq.client.sync import SyncClient
from machineq.core.device.api import SyncDevices
from machineq.core.device.models import (
    ActivationType,
    DeviceCreate,
    DevicePatch,
    DeviceUpdate,
)
from machineq.core.output_profile import OutputProfileCreate


@pytest.fixture
def devices_api(sync_client: SyncClient) -> SyncDevices:
    """Get devices API resource."""
    return sync_client.devices


class TestDevices:
    """Device API tests."""

    def test_get_all(self, devices_api: SyncDevices):
        """Test listing all devices."""
        devices_api.get_all()

    def test_get_existing_device(self, devices_api: SyncDevices):
        """Test retrieving a specific device."""
        devices = devices_api.get_all()
        if devices:
            deveui = devices[0].deveui
            result = devices_api.get(deveui)
            assert result.deveui == deveui

    def test_create_and_delete(self, devices_api: SyncDevices, get_service_profile, get_device_profile):
        """Test creating and deleting a device."""
        deveui = random_deveui()
        data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=get_service_profile(),
            device_profile=get_device_profile(),
            application_eui=random_hex(16),
            application_key=random_hex(32),
        )

        created_deveui = devices_api.create(data)

        try:
            assert created_deveui == deveui
            device = devices_api.get(deveui)
            assert device.deveui == deveui
        finally:
            devices_api.delete(deveui)

    def test_get_health(self, devices_api: SyncDevices, get_service_profile, get_device_profile):
        """Test getting device health. Create a device and check it appears in the offline list."""
        deveui = random_deveui()
        data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=get_service_profile(),
            device_profile=get_device_profile(),
            application_eui=random_hex(16),
            application_key=random_hex(32),
        )

        created_deveui = devices_api.create(data)
        try:
            assert created_deveui == deveui

            result = devices_api.get_health()
            offline_deveuis = [d.deveui for d in result.offline]
            assert deveui in offline_deveuis
        finally:
            devices_api.delete(deveui)

    def test_get_health_count(self, devices_api: SyncDevices):
        """Test getting device health count."""
        devices_api.get_health_count()
        # for now just checking the response is returned and parsed

    def test_devices_update_and_patch(self, devices_api: SyncDevices, get_service_profile, get_device_profile):
        """Test updating and patching a device by creating and then modifying it."""
        deveui = random_deveui()
        data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=get_service_profile(),
            device_profile=get_device_profile(),
            application_eui=random_hex(16),
            application_key=random_hex(32),
        )

        created_deveui = devices_api.create(data)
        output_profile = ""

        try:
            # create output profile for update ad lates deletion
            output_profile = devices_api.client.output_profiles.create(OutputProfileCreate(name=random_name()))
            device = devices_api.get(created_deveui)
            assert device.deveui == created_deveui
            assert not device.private_data
            update_data = DeviceUpdate(
                name=random_name(),
                service_profile=device.service_profile,
                device_profile=device.device_profile,
                decoder_type=device.decoder_type,
                output_profile=output_profile,
                private_data=True,
            )

            updated = devices_api.update(created_deveui, update_data)
            assert updated

            fetched = devices_api.get(created_deveui)
            assert fetched.deveui == created_deveui
            assert fetched.name == update_data.name
            assert fetched.private_data
            assert fetched.output_profile == output_profile

            patch_data = DevicePatch(
                name=random_name(),
                remove_output_profile=True,
            )
            patched = devices_api.patch(created_deveui, patch_data)
            assert patched
            fetched = devices_api.get(created_deveui)
            assert fetched.deveui == created_deveui
            assert fetched.name == patch_data.name
            assert fetched.output_profile == ""

        finally:
            devices_api.delete(created_deveui)
            if output_profile:
                devices_api.client.output_profiles.delete(output_profile)
