"""Gateway Group API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.gateway_group.models import (
    GatewayGroupCreate,
    GatewayGroupCreateResponse,
    GatewayGroupInstance,
    GatewayGroupPatch,
    GatewayGroupResponse,
    GatewayGroupUpdate,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncGatewayGroups(BaseResource["SyncClient"]):
    """Gateway groups resource for gateway grouping."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/groups/gateways")

    def get_all(self) -> list[GatewayGroupInstance]:
        """List all gateway groups.

        Returns:
            list[GatewayGroupInstance]: List of all gateway group instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayGroupResponse(**data).gateway_groups

    def get(self, group_id: str) -> GatewayGroupInstance:
        """Retrieve a gateway group by its ID.

        Args:
            group_id: The unique identifier of the gateway group.

        Returns:
            GatewayGroupInstance: The gateway group instance matching the given ID.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayGroupInstance(**data)

    def create(self, data: GatewayGroupCreate) -> str:
        """Create a new gateway group.

        Args:
            data: The gateway group creation data.

        Returns:
            str: The ID of the newly created gateway group.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupCreateResponse(**result).id

    def update(self, group_id: str, data: GatewayGroupUpdate) -> GatewayGroupInstance:
        """Update a gateway group (full replacement).

        Args:
            group_id: The unique identifier of the gateway group.
            data: The complete gateway group data for replacement.

        Returns:
            GatewayGroupInstance: The updated gateway group instance.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupInstance(**result)

    def patch(self, group_id: str, data: GatewayGroupPatch) -> GatewayGroupInstance:
        """Partially update a gateway group.

        Args:
            group_id: The unique identifier of the gateway group.
            data: The partial gateway group data to update.

        Returns:
            GatewayGroupInstance: The updated gateway group instance.
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupInstance(**result)

    def delete(self, group_id: str) -> None:
        """Delete a gateway group.

        Args:
            group_id: The unique identifier of the gateway group to delete.

        Returns:
            None
        """
        url = self._build_url(f"{group_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)


class AsyncGatewayGroups(BaseResource["AsyncClient"]):
    """Async gateway groups resource for gateway grouping."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/groups/gateways")

    async def get_all(self) -> list[GatewayGroupInstance]:
        """List all gateway groups.

        Returns:
            list[GatewayGroupInstance]: List of all gateway group instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayGroupResponse(**data).gateway_groups

    async def get(self, group_id: str) -> GatewayGroupInstance:
        """Retrieve a gateway group by its ID.

        Args:
            group_id: The unique identifier of the gateway group.

        Returns:
            GatewayGroupInstance: The gateway group instance matching the given ID.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayGroupInstance(**data)

    async def create(self, data: GatewayGroupCreate) -> str:
        """Create a new gateway group.

        Args:
            data: The gateway group creation data.

        Returns:
            str: The ID of the newly created gateway group.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupCreateResponse(**result).id

    async def update(self, group_id: str, data: GatewayGroupUpdate) -> GatewayGroupInstance:
        """Update a gateway group (full replacement).

        Args:
            group_id: The unique identifier of the gateway group.
            data: The complete gateway group data for replacement.

        Returns:
            GatewayGroupInstance: The updated gateway group instance.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupInstance(**result)

    async def patch(self, group_id: str, data: GatewayGroupPatch) -> GatewayGroupInstance:
        """Partially update a gateway group.

        Args:
            group_id: The unique identifier of the gateway group.
            data: The partial gateway group data to update.

        Returns:
            GatewayGroupInstance: The updated gateway group instance.
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayGroupInstance(**result)

    async def delete(self, group_id: str) -> None:
        """Delete a gateway group.

        Args:
            group_id: The unique identifier of the gateway group to delete.

        Returns:
            None
        """
        url = self._build_url(f"{group_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)
