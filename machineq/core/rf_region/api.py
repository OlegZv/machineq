"""RF Region API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.rf_region.models import (
    ListRFRegionsResponse,
    RFRegionInstance,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncRFRegions(BaseResource["SyncClient"]):
    """RF regions resource for LoRa frequency bands."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/rfregions")

    def get_all(self) -> list[RFRegionInstance]:
        """List all RF regions.

        Returns:
            list[RFRegionInstance]: List of all RF region instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ListRFRegionsResponse(**data).rf_regions


class AsyncRFRegions(BaseResource["AsyncClient"]):
    """Async RF regions resource for LoRa frequency bands."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/rfregions")

    async def get_all(self) -> list[RFRegionInstance]:
        """List all RF regions.

        Returns:
            list[RFRegionInstance]: List of all RF region instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ListRFRegionsResponse(**data).rf_regions
