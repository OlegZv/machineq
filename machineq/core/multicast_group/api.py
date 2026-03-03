"""Multicast Group API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.multicast_group.models import (
    AddDevicesWithMulticastGroupRequest,
    AddDevicesWithMulticastGroupResponse,
    AddGatewaysWithMulticastGroupRequest,
    AddGatewaysWithMulticastGroupResponse,
    CreateMulticastGroupRequest,
    GetGatewaysByMulticastGroupResponse,
    GetMulticastGroupResponse,
    GetMulticastGroupsResponse,
    MulticastGroup,
    RemoveDevicesFromMulticastGroupRequest,
    RemoveDevicesFromMulticastGroupResponse,
    RemoveGatewaysFromMulticastGroupRequest,
    RemoveGatewaysFromMulticastGroupResponse,
    UpdateMulticastGroupRequest,
)
from machineq.core.shared.models import CommonOKResponse

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncMulticastGroups(BaseResource["SyncClient"]):
    """Multicast groups resource for multicast group management."""

    def __init__(self, client: SyncClient):
        # Note: multicast uses /v0, not /v1
        super().__init__(
            client,
            "/multicastgroups",
            version="v0",
        )

    def get_all(self) -> list[MulticastGroup]:
        """List all multicast groups.

        Returns:
            list[MulticastGroup]: List of all multicast group instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetMulticastGroupsResponse(**data).multicast_groups

    def get(self, multicast_deveui: str) -> MulticastGroup:
        """Retrieve a multicast group by its MulticastDevEUI.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            MulticastGroup: The multicast group instance matching the given DevEUI.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetMulticastGroupResponse(**data).multicast_group

    def create(self, data: CreateMulticastGroupRequest) -> bool:
        """Create a new multicast group.

        Args:
            data: The multicast group creation request data.

        Returns:
            bool: True if the creation was successful, False otherwise.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def update(
        self,
        multicast_deveui: str,
        data: UpdateMulticastGroupRequest,
    ) -> bool:
        """Update a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The multicast group update request data.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def delete(self, multicast_deveui: str) -> bool:
        """Delete a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = self.client.http_client.delete(url, headers=self._build_headers())
        data = self._parse_response(response)
        return CommonOKResponse(**data).response

    def add_devices(
        self,
        multicast_deveui: str,
        data: AddDevicesWithMulticastGroupRequest,
    ) -> AddDevicesWithMulticastGroupResponse:
        """Add devices to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The device addition request data.

        Returns:
            AddDevicesWithMulticastGroupResponse: The device addition response.
        """
        url = self._build_url(f"{multicast_deveui}/devices/associate")
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return AddDevicesWithMulticastGroupResponse(**result)

    def remove_devices(
        self,
        multicast_deveui: str,
        data: RemoveDevicesFromMulticastGroupRequest,
    ) -> RemoveDevicesFromMulticastGroupResponse:
        """Remove devices from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The device removal request data.

        Returns:
            RemoveDevicesFromMulticastGroupResponse: The device removal response.
        """
        url = self._build_url(f"{multicast_deveui}/devices/deassociate")
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RemoveDevicesFromMulticastGroupResponse(**result)

    def add_gateways(
        self,
        multicast_deveui: str,
        data: AddGatewaysWithMulticastGroupRequest,
    ) -> AddGatewaysWithMulticastGroupResponse:
        """Add gateways to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The gateway addition request data.

        Returns:
            AddGatewaysWithMulticastGroupResponse: The gateway addition response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/associate")
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return AddGatewaysWithMulticastGroupResponse(**result)

    def remove_gateways(
        self,
        multicast_deveui: str,
        data: RemoveGatewaysFromMulticastGroupRequest,
    ) -> RemoveGatewaysFromMulticastGroupResponse:
        """Remove gateways from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The gateway removal request data.

        Returns:
            RemoveGatewaysFromMulticastGroupResponse: The gateway removal response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/deassociate")
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RemoveGatewaysFromMulticastGroupResponse(**result)

    def get_all_gateways(
        self,
        multicast_deveui: str,
    ):
        """List gateways associated with a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            GetGatewaysByMulticastGroupResponse: Gateways in the multicast group.
        """
        url = self._build_url(f"{multicast_deveui}/gateways")
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetGatewaysByMulticastGroupResponse(**data)


class AsyncMulticastGroups(BaseResource["AsyncClient"]):
    """Async multicast groups resource for multicast group management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/multicastgroups", version="v0")

    async def get_all(self) -> list[MulticastGroup]:
        """List all multicast groups.

        Returns:
            list[MulticastGroup]: List of all multicast group instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetMulticastGroupsResponse(**data).multicast_groups

    async def get(self, multicast_deveui: str) -> MulticastGroup:
        """Retrieve a multicast group by its MulticastDevEUI.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            MulticastGroup: The multicast group instance matching the given DevEUI.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetMulticastGroupResponse(**data).multicast_group

    async def create(self, data: CreateMulticastGroupRequest) -> bool:
        """Create a new multicast group.

        Args:
            data: The multicast group creation request data.

        Returns:
            bool: True if the creation was successful, False otherwise.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    async def update(
        self,
        multicast_deveui: str,
        data: UpdateMulticastGroupRequest,
    ) -> bool:
        """Update a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The multicast group update request data.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    async def delete(self, multicast_deveui: str) -> bool:
        """Delete a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        url = self._build_url(f"{multicast_deveui}")
        response = await self.client.http_client.delete(url, headers=self._build_headers())
        data = self._parse_response(response)
        return CommonOKResponse(**data).response

    async def add_devices(
        self,
        multicast_deveui: str,
        data: AddDevicesWithMulticastGroupRequest,
    ) -> AddDevicesWithMulticastGroupResponse:
        """Add devices to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The device addition request data.

        Returns:
            AddDevicesWithMulticastGroupResponse: The device addition response.
        """
        url = self._build_url(f"{multicast_deveui}/devices/associate")
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return AddDevicesWithMulticastGroupResponse(**result)

    async def remove_devices(
        self,
        multicast_deveui: str,
        data: RemoveDevicesFromMulticastGroupRequest,
    ) -> RemoveDevicesFromMulticastGroupResponse:
        """Remove devices from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The device removal request data.

        Returns:
            RemoveDevicesFromMulticastGroupResponse: The device removal response.
        """
        url = self._build_url(f"{multicast_deveui}/devices/deassociate")
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RemoveDevicesFromMulticastGroupResponse(**result)

    async def add_gateways(
        self,
        multicast_deveui: str,
        data: AddGatewaysWithMulticastGroupRequest,
    ) -> AddGatewaysWithMulticastGroupResponse:
        """Add gateways to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The gateway addition request data.

        Returns:
            AddGatewaysWithMulticastGroupResponse: The gateway addition response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/associate")
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return AddGatewaysWithMulticastGroupResponse(**result)

    async def remove_gateways(
        self,
        multicast_deveui: str,
        data: RemoveGatewaysFromMulticastGroupRequest,
    ) -> RemoveGatewaysFromMulticastGroupResponse:
        """Remove gateways from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            data: The gateway removal request data.

        Returns:
            RemoveGatewaysFromMulticastGroupResponse: The gateway removal response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/deassociate")
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RemoveGatewaysFromMulticastGroupResponse(**result)

    async def get_all_gateways(
        self,
        multicast_deveui: str,
    ):
        """List gateways associated with a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            GetGatewaysByMulticastGroupResponse: Gateways in the multicast group.
        """
        url = self._build_url(f"{multicast_deveui}/gateways")
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetGatewaysByMulticastGroupResponse(**data)
