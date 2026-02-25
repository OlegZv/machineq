"""Device API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.device.models import (
    DeviceCreate,
    DeviceCreateResponse,
    DeviceInstance,
    DeviceMessage,
    DevicePatch,
    DevicePayloadResponse,
    DeviceResponse,
    DevicesHealthCountResponse,
    DevicesHealthResponse,
    DeviceUpdate,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncDevices(BaseResource["SyncClient"]):
    """Devices resource for LoRaWAN device management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/devices")

    def get_all(self) -> list[DeviceInstance]:
        """List all devices.

        Returns:
            list[DeviceInstance]: List of all device instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceResponse(**data).devices

    def get(self, deveui: str) -> DeviceInstance:
        """Retrieve a device by its DevEUI.

        Args:
            deveui: The device EUI (unique identifier).

        Returns:
            DeviceInstance: The device instance matching the given DevEUI.
        """
        url = self._build_url(f"{deveui}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceInstance(**data)

    def create(self, data: DeviceCreate) -> str:
        """Create a new device.

        Args:
            data: The device creation data.

        Returns:
            str: The DevEUI of the newly created device.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceCreateResponse(**result).id

    def update(self, deveui: str, data: DeviceUpdate) -> DeviceInstance:
        """Update a device (full replacement).

        Args:
            deveui: The device EUI (unique identifier).
            data: The complete device data for replacement.

        Returns:
            DeviceInstance: The updated device instance.
        """
        url = self._build_url(f"{deveui}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceInstance(**result)

    def patch(self, deveui: str, data: DevicePatch) -> DeviceInstance:
        """Partially update a device.

        Args:
            deveui: The device EUI (unique identifier).
            data: The partial device data to update.

        Returns:
            DeviceInstance: The updated device instance.
        """
        url = self._build_url(f"{deveui}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceInstance(**result)

    def delete(self, deveui: str) -> None:
        """Delete a device.

        Args:
            deveui: The device EUI (unique identifier) to delete.

        Returns:
            None
        """
        url = self._build_url(f"{deveui}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    def send_message(self, deveui: str, data: DeviceMessage) -> None:
        """Send a downstream message to a device.

        Args:
            deveui: The device EUI (unique identifier).
            data: The message data to send.

        Returns:
            None
        """
        url = self._build_url(f"{deveui}/message")
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        self._parse_response(response)

    def get_payloads(
        self,
        deveui: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve device payloads within a time range.

        Args:
            deveui: The device EUI (unique identifier).
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            DevicePayloadResponse: The device payloads within the specified time range.
        """
        url = self._build_url(f"{deveui}/payloads")
        params = {}
        if start_time:
            params["StartTime"] = start_time
        if end_time:
            params["EndTime"] = end_time

        response = self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return DevicePayloadResponse(**data)

    def get_health(self) -> DevicesHealthResponse:
        """Retrieve devices grouped by health status.

        Returns:
            DevicesHealthResponse: Devices grouped by their health status.
        """
        url = self._build_url("health")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DevicesHealthResponse(**data)

    def get_health_count(self):
        """Retrieve device count grouped by health status.

        Returns:
            DevicesHealthCountResponse: Device counts grouped by health status.
        """
        url = self._build_url("healthcount")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DevicesHealthCountResponse(**data)


class AsyncDevices(BaseResource["AsyncClient"]):
    """Async devices resource for LoRaWAN device management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/devices")

    async def get_all(self):
        """List all devices.

        Returns:
            DeviceResponse: All device instances with response metadata.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceResponse(**data)

    async def get(self, deveui: str) -> DeviceInstance:
        """Retrieve a device by its DevEUI.

        Args:
            deveui: The device EUI (unique identifier).

        Returns:
            DeviceInstance: The device instance matching the given DevEUI.
        """
        url = self._build_url(f"{deveui}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceInstance(**data)

    async def create(self, data: DeviceCreate) -> str:
        """Create a new device.

        Args:
            data: The device creation data.

        Returns:
            str: The DevEUI of the newly created device.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceCreateResponse(**result).id

    async def update(self, deveui: str, data: DeviceUpdate) -> DeviceInstance:
        """Update a device (full replacement).

        Args:
            deveui: The device EUI (unique identifier).
            data: The complete device data for replacement.

        Returns:
            DeviceInstance: The updated device instance.
        """
        url = self._build_url(f"{deveui}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceInstance(**result)

    async def patch(self, deveui: str, data: DevicePatch) -> DeviceInstance:
        """Partially update a device.

        Args:
            deveui: The device EUI (unique identifier).
            data: The partial device data to update.

        Returns:
            DeviceInstance: The updated device instance.
        """
        url = self._build_url(f"{deveui}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceInstance(**result)

    async def delete(self, deveui: str) -> None:
        """Delete a device.

        Args:
            deveui: The device EUI (unique identifier) to delete.

        Returns:
            None
        """
        url = self._build_url(f"{deveui}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    async def send_message(self, deveui: str, data: DeviceMessage) -> None:
        """Send a downstream message to a device.

        Args:
            deveui: The device EUI (unique identifier).
            data: The message data to send.

        Returns:
            None
        """
        url = self._build_url(f"{deveui}/message")
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        self._parse_response(response)

    async def get_payloads(
        self,
        deveui: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve device payloads within a time range.

        Args:
            deveui: The device EUI (unique identifier).
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            DevicePayloadResponse: The device payloads within the specified time range.
        """
        url = self._build_url(f"{deveui}/payloads")
        params = {}
        if start_time:
            params["StartTime"] = start_time
        if end_time:
            params["EndTime"] = end_time

        response = await self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return DevicePayloadResponse(**data)

    async def get_health(self):
        """Retrieve devices grouped by health status.

        Returns:
            DevicesHealthResponse: Devices grouped by their health status.
        """
        url = self._build_url("health")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DevicesHealthResponse(**data)

    async def get_health_count(self):
        """Retrieve device count grouped by health status.

        Returns:
            DevicesHealthCountResponse: Device counts grouped by health status.
        """
        url = self._build_url("healthcount")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DevicesHealthCountResponse(**data)
