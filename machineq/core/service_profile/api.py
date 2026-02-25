"""Service Profile API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.service_profile.models import (
    ServiceProfileInstance,
    ServiceProfilesResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncServiceProfiles(BaseResource["SyncClient"]):
    """Service profiles resource for service profile management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/serviceprofiles")

    def get_all(self) -> list[ServiceProfileInstance]:
        """List all service profiles."""
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ServiceProfilesResponse(**data).service_profiles


class AsyncServiceProfiles(BaseResource["AsyncClient"]):
    """Async service profiles resource for service profile management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/serviceprofiles")

    async def get_all(self) -> list[ServiceProfileInstance]:
        """List all service profiles."""
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ServiceProfilesResponse(**data).service_profiles
