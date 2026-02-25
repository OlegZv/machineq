"""Version API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.version.models import VersionResponse

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncVersion(BaseResource["SyncClient"]):
    """Version resource for API version information."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/version")

    def get(self) -> VersionResponse:
        """Get API version."""
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return VersionResponse(**data)


class AsyncVersion(BaseResource["AsyncClient"]):
    """Async version resource for API version information."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/version")

    async def get(self) -> VersionResponse:
        """Get API version."""
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return VersionResponse(**data)
