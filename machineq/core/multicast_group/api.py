"""Multicast Group API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.multicast_group.models import (
    AddGatewaysWithMulticastGroupRequest,
    AddGatewaysWithMulticastGroupResponse,
    CreateMulticastGroupRequest,
    GetGatewaysByMulticastGroupResponse,
    GetMulticastGroupResponse,
    GetMulticastGroupsResponse,
    MulticastGroup,
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
        data = super()._get_all_generic()
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

    def add_gateways(
        self,
        multicast_deveui: str,
        node_ids: list[str],
    ) -> AddGatewaysWithMulticastGroupResponse:
        """Add gateways to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            node_ids: The list of node ids to add to the multicast group.

        Returns:
            AddGatewaysWithMulticastGroupResponse: The gateway addition response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/associate")
        data = AddGatewaysWithMulticastGroupRequest(gateways=node_ids)
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
        node_ids: list[str],
    ) -> RemoveGatewaysFromMulticastGroupResponse:
        """Remove gateways from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            node_ids: The list of node ids to remove from the multicast group.

        Returns:
            RemoveGatewaysFromMulticastGroupResponse: The gateway removal response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/deassociate")
        data = RemoveGatewaysFromMulticastGroupRequest(gateways=node_ids)
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
    ) -> list[str]:
        """List gateways associated with a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            list[str]: NodeIDs in the multicast group.
        """
        url = self._build_url(f"{multicast_deveui}/gateways")
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetGatewaysByMulticastGroupResponse(**data).gateways


class AsyncMulticastGroups(BaseResource["AsyncClient"]):
    """Async multicast groups resource for multicast group management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/multicastgroups", version="v0")

    async def get_all(self) -> list[MulticastGroup]:
        """List all multicast groups.

        Returns:
            list[MulticastGroup]: List of all multicast group instances.
        """
        data = await super()._get_all_generic_async()
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

    async def add_gateways(
        self,
        multicast_deveui: str,
        node_ids: list[str],
    ) -> AddGatewaysWithMulticastGroupResponse:
        """Add gateways to a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            node_ids: The list of node ids to add to the multicast group.

        Returns:
            AddGatewaysWithMulticastGroupResponse: The gateway addition response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/associate")
        data = AddGatewaysWithMulticastGroupRequest(gateways=node_ids)
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
        node_ids: list[str],
    ) -> RemoveGatewaysFromMulticastGroupResponse:
        """Remove gateways from a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.
            node_ids: The list of node ids to remove from the multicast group.

        Returns:
            RemoveGatewaysFromMulticastGroupResponse: The gateway removal response.
        """
        url = self._build_url(f"{multicast_deveui}/gateways/deassociate")
        data = RemoveGatewaysFromMulticastGroupRequest(gateways=node_ids)
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
    ) -> list[str]:
        """List gateways associated with a multicast group.

        Args:
            multicast_deveui: The unique multicast device EUI.

        Returns:
            list[str]: NodeIDs in the multicast group.
        """
        url = self._build_url(f"{multicast_deveui}/gateways")
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return GetGatewaysByMulticastGroupResponse(**data).gateways
