"""Device Profile API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.device_profile.models import (
    DeviceProfileDevicesUpdate,
    DeviceProfileDevicesUpdateResponse,
    DeviceProfileInstance,
    DeviceProfileResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncDeviceProfiles(BaseResource["SyncClient"]):
    """Device profiles resource for device profile management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/deviceprofiles")

    def get_all(self) -> list[DeviceProfileInstance]:
        """List all device profiles.

        Returns:
            list[DeviceProfileInstance]: List of all device profile instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceProfileResponse(**data).device_profiles

    def update_devices(
        self,
        profile_id: str,
        data: DeviceProfileDevicesUpdate,
    ) -> DeviceProfileDevicesUpdateResponse:
        """Update devices associated with a device profile.

        Args:
            profile_id: The unique identifier of the device profile.
            data: The device association update data.

        Returns:
            DeviceProfileDevicesUpdateResponse: The response containing updated device associations.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceProfileDevicesUpdateResponse(**result)


class AsyncDeviceProfiles(BaseResource["AsyncClient"]):
    """Async device profiles resource for device profile management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/deviceprofiles")

    async def get_all(self) -> list[DeviceProfileInstance]:
        """List all device profiles.

        Returns:
            list[DeviceProfileInstance]: List of all device profile instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceProfileResponse(**data).device_profiles

    async def update_devices(
        self,
        profile_id: str,
        data: DeviceProfileDevicesUpdate,
    ) -> DeviceProfileDevicesUpdateResponse:
        """Update devices associated with a device profile.

        Args:
            profile_id: The unique identifier of the device profile.
            data: The device association update data.

        Returns:
            DeviceProfileDevicesUpdateResponse: The response containing updated device associations.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceProfileDevicesUpdateResponse(**result)
