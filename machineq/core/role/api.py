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

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncRoles(BaseResource["SyncClient"]):
    """Roles resource for RBAC role management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/roles")

    def get_all(self) -> list[RoleInstance]:
        """List all roles."""
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return RoleResponse(**data).roles

    def get(self, role_id: str) -> RoleInstance:
        """Get role by ID."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return RoleInstance(**data)

    def create(self, data: RoleCreate) -> str:
        """Create a new role."""
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleCreateResponse(**result).id

    def update(self, role_id: str, data: RoleUpdate) -> RoleInstance:
        """Update role (full replacement)."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleInstance(**result)

    def patch(self, role_id: str, data: RolePatch) -> RoleInstance:
        """Partially update role."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleInstance(**result)

    def delete(self, role_id: str) -> None:
        """Delete role."""
        url = self._build_url(f"{role_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)


class AsyncRoles(BaseResource["AsyncClient"]):
    """Async roles resource for RBAC role management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/roles")

    async def get_all(self) -> list[RoleInstance]:
        """List all roles."""
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return RoleResponse(**data).roles

    async def get(self, role_id: str) -> RoleInstance:
        """Get role by ID."""
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return RoleInstance(**data)

    async def create(self, data: RoleCreate) -> str:
        """Create a new role."""
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleCreateResponse(**result).id

    async def update(self, role_id: str, data: RoleUpdate) -> RoleInstance:
        """Update role (full replacement)."""
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleInstance(**result)

    async def patch(self, role_id: str, data: RolePatch) -> RoleInstance:
        """Partially update role."""
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return RoleInstance(**result)

    async def delete(self, role_id: str) -> None:
        """Delete role."""
        url = self._build_url(f"{role_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)
