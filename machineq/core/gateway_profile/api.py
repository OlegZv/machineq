"""Gateway Profile API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.gateway_profile.models import (
    GatewayProfileInstance,
    GatewayProfileResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncGatewayProfiles(BaseResource["SyncClient"]):
    """Gateway profiles resource for gateway profile management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/gatewayprofiles")

    def get_all(self) -> list[GatewayProfileInstance]:
        """List all gateway profiles.

        Returns:
            list[GatewayProfileInstance]: List of all gateway profile instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayProfileResponse(**data).gateway_profiles


class AsyncGatewayProfiles(BaseResource["AsyncClient"]):
    """Async gateway profiles resource for gateway profile management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/gatewayprofiles")

    async def get_all(self) -> list[GatewayProfileInstance]:
        """List all gateway profiles.

        Returns:
            list[GatewayProfileInstance]: List of all gateway profile instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayProfileResponse(**data).gateway_profiles
