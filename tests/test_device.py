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
)


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

    def test_create_and_delete(self, devices_api: SyncDevices):
        """Test creating and deleting a device."""
        deveui = random_deveui()
        data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=self.get_service_profile(devices_api.client),
            device_profile=self.get_device_profile(devices_api.client),
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

    def test_get_health(self, devices_api: SyncDevices):
        """Test getting device health. Create a device and check it appears in the offline list."""
        deveui = random_deveui()
        data = DeviceCreate(
            name=random_name(),
            deveui=deveui,
            activation_type=ActivationType.OTAA,
            service_profile=self.get_service_profile(devices_api.client),
            device_profile=self.get_device_profile(devices_api.client),
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

    def get_service_profile(self, client: SyncClient) -> str:
        """Test getting device service profile."""
        profiles = client.service_profiles.get_all()
        assert len(profiles) > 0
        return profiles[0].id

    def get_device_profile(self, client: SyncClient) -> str:
        """Test getting device profile."""
        profiles = client.device_profiles.get_all()
        assert len(profiles) > 0
        return profiles[0].id
