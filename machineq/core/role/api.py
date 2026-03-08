"""Role API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.role.models import (
    RoleCreate,
    RoleCreateResponse,
    RoleInstance,
    RolePatch,
    RoleResponse,
    RoleUpdate,
)
from machineq.core.shared.models import CommonOKResponse

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncRoles(BaseResource["SyncClient"]):
    """Roles resource for RBAC role management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/roles")

    def get_all(self) -> list[RoleInstance]:
        """List all roles."""
        data = super()._get_all_generic()
        return RoleResponse(**data).roles

    def get(self, role_id: str) -> RoleInstance:
        """Get role by ID."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return RoleInstance(**data)

    def create(self, data: RoleCreate) -> str:
        """Create a new role."""
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RoleCreateResponse(**result).id

    def update(self, role_id: str, data: RoleUpdate) -> bool:
        """Update role (full replacement)."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def patch(self, role_id: str, data: RolePatch) -> bool:
        """Partially update role."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def delete(self, role_id: str) -> None:
        """Delete role."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers())
        self._parse_response(response)


class AsyncRoles(BaseResource["AsyncClient"]):
    """Async roles resource for RBAC role management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/roles")

    async def get_all(self) -> list[RoleInstance]:
        """List all roles."""
        data = await super()._get_all_generic_async()
        return RoleResponse(**data).roles

    async def get(self, role_id: str) -> RoleInstance:
        """Get role by ID.

        Args:
            role_id: The unique identifier of the role to retrieve.

        Returns: The role instance corresponding to the provided ID.
        """
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return RoleInstance(**data)

    async def create(self, data: RoleCreate) -> str:
        """Create a new role.

        Args:
            data: The role creation data.
        Returns: The ID of the created role.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return RoleCreateResponse(**result).id

    async def update(self, role_id: str, data: RoleUpdate) -> bool:
        """Fully update a role.

        Args:
            role_id (str): The unique identifier of the role to update.
            data (RoleUpdate): The complete role data for replacement.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    async def patch(self, role_id: str, data: RolePatch) -> bool:
        """
        Partially update a role.

        Args:
            role_id (str): The unique identifier of the role to patch.
            data (RolePatch): The partial role data to update.

        Returns:
            bool: True if the patch was successful, False otherwise.
        """
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    async def delete(self, role_id: str) -> None:
        """Delete role by ID.

        Args:
            role_id (str): The unique identifier of the role to delete.
        """
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers())
        self._parse_response(response)
