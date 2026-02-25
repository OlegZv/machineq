"""Device Group API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.device_group.models import (
    DeviceGroupCreate,
    DeviceGroupCreateResponse,
    DeviceGroupInstance,
    DeviceGroupPatch,
    DeviceGroupResponse,
    DeviceGroupUpdate,
    GetDeviceGroupRecentResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncDeviceGroups(BaseResource["SyncClient"]):
    """Device groups resource for device grouping."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/groups/devices")

    def get_all(self) -> list[DeviceGroupInstance]:
        """List all device groups.

        Returns:
            list[DeviceGroupInstance]: List of all device group instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceGroupResponse(**data).device_groups

    def get(self, group_id: str) -> DeviceGroupInstance:
        """Retrieve a device group by its ID.

        Args:
            group_id: The unique identifier of the device group.

        Returns:
            DeviceGroupInstance: The device group instance matching the given ID.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceGroupInstance(**data)

    def create(self, data: DeviceGroupCreate) -> str:
        """Create a new device group.

        Args:
            data: The device group creation data.

        Returns:
            str: The ID of the newly created device group.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupCreateResponse(**result).id

    def update(self, group_id: str, data: DeviceGroupUpdate) -> DeviceGroupInstance:
        """Update a device group (full replacement).

        Args:
            group_id: The unique identifier of the device group.
            data: The complete device group data for replacement.

        Returns:
            DeviceGroupInstance: The updated device group instance.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupInstance(**result)

    def patch(self, group_id: str, data: DeviceGroupPatch) -> DeviceGroupInstance:
        """Partially update a device group.

        Args:
            group_id: The unique identifier of the device group.
            data: The partial device group data to update.

        Returns:
            DeviceGroupInstance: The updated device group instance.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupInstance(**result)

    def delete(self, group_id: str) -> None:
        """Delete a device group.

        Args:
            group_id: The unique identifier of the device group to delete.

        Returns:
            None
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    def get_recent(
        self,
        group_id: str,
        payload: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve devices with recent data in a group.

        Args:
            group_id: The unique identifier of the device group.
            payload: Optional payload filter.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            GetDeviceGroupRecentResponse: Devices with recent data in the group.
        """
        url = self._build_url(f"{group_id}/recent")
        params = {}
        if payload:
            params["Payload"] = payload
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
        return GetDeviceGroupRecentResponse(**data)


class AsyncDeviceGroups(BaseResource["AsyncClient"]):
    """Async device groups resource for device grouping."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/groups/devices")

    async def get_all(self) -> list[DeviceGroupInstance]:
        """List all device groups.

        Returns:
            list[DeviceGroupInstance]: List of all device group instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceGroupResponse(**data).device_groups

    async def get(self, group_id: str) -> DeviceGroupInstance:
        """Retrieve a device group by its ID.

        Args:
            group_id: The unique identifier of the device group.

        Returns:
            DeviceGroupInstance: The device group instance matching the given ID.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DeviceGroupInstance(**data)

    async def create(self, data: DeviceGroupCreate) -> str:
        """Create a new device group.

        Args:
            data: The device group creation data.

        Returns:
            str: The ID of the newly created device group.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupCreateResponse(**result).id

    async def update(self, group_id: str, data: DeviceGroupUpdate) -> DeviceGroupInstance:
        """Update a device group (full replacement).

        Args:
            group_id: The unique identifier of the device group.
            data: The complete device group data for replacement.

        Returns:
            DeviceGroupInstance: The updated device group instance.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupInstance(**result)

    async def patch(self, group_id: str, data: DeviceGroupPatch) -> DeviceGroupInstance:
        """Partially update a device group.

        Args:
            group_id: The unique identifier of the device group.
            data: The partial device group data to update.

        Returns:
            DeviceGroupInstance: The updated device group instance.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return DeviceGroupInstance(**result)

    async def delete(self, group_id: str) -> None:
        """Delete a device group.

        Args:
            group_id: The unique identifier of the device group to delete.

        Returns:
            None
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    async def get_recent(
        self,
        group_id: str,
        payload: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve devices with recent data in a group.

        Args:
            group_id: The unique identifier of the device group.
            payload: Optional payload filter.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            GetDeviceGroupRecentResponse: Devices with recent data in the group.
        """
        url = self._build_url(f"{group_id}/recent")
        params = {}
        if payload:
            params["Payload"] = payload
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
        return GetDeviceGroupRecentResponse(**data)
