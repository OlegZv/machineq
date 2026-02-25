"""Gateway API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.gateway.models import (
    GatewayCreate,
    GatewayCreateResponse,
    GatewayDeviceResponse,
    GatewayInstance,
    GatewayPatch,
    GatewaysConnectionResponse,
    GatewaysHealthResponse,
    GatewayStatistics,
    GatewayUpdate,
    MachineqapiGatewayResponse,
    MachineqapiGetGatewayEventsResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncGateways(BaseResource["SyncClient"]):
    """Gateways resource for LoRaWAN gateway management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/gateways")

    def get_all(self) -> list[GatewayInstance]:
        """List all gateways.

        Returns:
            list[GatewayInstance]: List of all gateway instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return MachineqapiGatewayResponse(**data).gateways

    def get(self, gateway_id: str) -> GatewayInstance:
        """Retrieve a gateway by ID or Node ID.

        Args:
            gateway_id: The unique identifier or Node ID of the gateway.

        Returns:
            GatewayInstance: The gateway instance matching the given ID.
        """
        url = self._build_url(f"{gateway_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayInstance(**data)

    def create(self, data: GatewayCreate) -> str:
        """Create a new gateway.

        Args:
            data: The gateway creation data.

        Returns:
            str: The ID of the newly created gateway.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayCreateResponse(**result).id

    def update(self, gateway_id: str, data: GatewayUpdate) -> GatewayInstance:
        """Update a gateway (full replacement).

        Args:
            gateway_id: The unique identifier of the gateway.
            data: The complete gateway data for replacement.

        Returns:
            GatewayInstance: The updated gateway instance.
        """
        url = self._build_url(f"{gateway_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayInstance(**result)

    def patch(self, gateway_id: str, data: GatewayPatch) -> GatewayInstance:
        """Partially update a gateway.

        Args:
            gateway_id: The unique identifier of the gateway.
            data: The partial gateway data to update.

        Returns:
            GatewayInstance: The updated gateway instance.
        """
        url = self._build_url(f"{gateway_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayInstance(**result)

    def delete(self, gateway_id: str) -> None:
        """Delete a gateway.

        Args:
            gateway_id: The unique identifier of the gateway to delete.

        Returns:
            None
        """
        url = self._build_url(f"{gateway_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    def get_devices(
        self,
        gateway_id: str,
        days: int | None = None,
    ):
        """Retrieve devices seen by a gateway.

        Args:
            gateway_id: The unique identifier of the gateway.
            days: Optional number of days to look back.

        Returns:
            GatewayDeviceResponse: Devices seen by the gateway.
        """
        url = self._build_url(f"{gateway_id}/devices")
        params = {}
        if days is not None:
            params["Days"] = days

        response = self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return GatewayDeviceResponse(**data)

    def get_statistics(self, gateway_id: str):
        """Retrieve gateway statistics.

        Args:
            gateway_id: The unique identifier of the gateway.

        Returns:
            GatewayStatistics: Statistics for the gateway.
        """
        url = self._build_url(f"{gateway_id}/statistics")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayStatistics(**data)

    def get_events(
        self,
        node_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve gateway events.

        Args:
            node_id: The node ID of the gateway.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            MachineqapiGetGatewayEventsResponse: Gateway events within the specified time range.
        """
        url = self._build_url(f"{node_id}/events")
        params = {}
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
        return MachineqapiGetGatewayEventsResponse(**data)

    def get_connection_status(self):
        """Retrieve gateways grouped by connection status.

        Returns:
            GatewaysConnectionResponse: Gateways grouped by their connection status.
        """
        url = self._build_url("connection")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewaysConnectionResponse(**data)

    def get_health(self):
        """Retrieve gateways grouped by health status.

        Returns:
            GatewaysHealthResponse: Gateways grouped by their health status.
        """
        url = self._build_url("health")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewaysHealthResponse(**data)


class AsyncGateways(BaseResource["AsyncClient"]):
    """Async gateways resource for LoRaWAN gateway management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/gateways")

    async def get_all(self) -> list[GatewayInstance]:
        """List all gateways.

        Returns:
            list[GatewayInstance]: List of all gateway instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return MachineqapiGatewayResponse(**data).gateways

    async def get(self, gateway_id: str) -> GatewayInstance:
        """Retrieve a gateway by ID or Node ID.

        Args:
            gateway_id: The unique identifier or Node ID of the gateway.

        Returns:
            GatewayInstance: The gateway instance matching the given ID.
        """
        url = self._build_url(f"{gateway_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayInstance(**data)

    async def create(self, data: GatewayCreate) -> str:
        """Create a new gateway.

        Args:
            data: The gateway creation data.

        Returns:
            str: The ID of the newly created gateway.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayCreateResponse(**result).id

    async def update(self, gateway_id: str, data: GatewayUpdate) -> GatewayInstance:
        """Update a gateway (full replacement).

        Args:
            gateway_id: The unique identifier of the gateway.
            data: The complete gateway data for replacement.

        Returns:
            GatewayInstance: The updated gateway instance.
        """
        url = self._build_url(f"{gateway_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayInstance(**result)

    async def patch(self, gateway_id: str, data: GatewayPatch) -> GatewayInstance:
        """Partially update a gateway.

        Args:
            gateway_id: The unique identifier of the gateway.
            data: The partial gateway data to update.

        Returns:
            GatewayInstance: The updated gateway instance.
        """
        url = self._build_url(f"{gateway_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return GatewayInstance(**result)

    async def delete(self, gateway_id: str) -> None:
        """Delete a gateway.

        Args:
            gateway_id: The unique identifier of the gateway to delete.

        Returns:
            None
        """
        url = self._build_url(f"{gateway_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    async def get_devices(
        self,
        gateway_id: str,
        days: int | None = None,
    ):
        """Retrieve devices seen by a gateway.

        Args:
            gateway_id: The unique identifier of the gateway.
            days: Optional number of days to look back.

        Returns:
            GatewayDeviceResponse: Devices seen by the gateway.
        """
        url = self._build_url(f"{gateway_id}/devices")
        params = {}
        if days is not None:
            params["Days"] = days

        response = await self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return GatewayDeviceResponse(**data)

    async def get_statistics(self, gateway_id: str):
        """Retrieve gateway statistics.

        Args:
            gateway_id: The unique identifier of the gateway.

        Returns:
            GatewayStatistics: Statistics for the gateway.
        """
        url = self._build_url(f"{gateway_id}/statistics")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewayStatistics(**data)

    async def get_events(
        self,
        node_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """Retrieve gateway events.

        Args:
            node_id: The node ID of the gateway.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.

        Returns:
            MachineqapiGetGatewayEventsResponse: Gateway events within the specified time range.
        """
        url = self._build_url(f"{node_id}/events")
        params = {}
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
        return MachineqapiGetGatewayEventsResponse(**data)

    async def get_connection_status(self):
        """Retrieve gateways grouped by connection status.

        Returns:
            GatewaysConnectionResponse: Gateways grouped by their connection status.
        """
        url = self._build_url("connection")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewaysConnectionResponse(**data)

    async def get_health(self):
        """Retrieve gateways grouped by health status.

        Returns:
            GatewaysHealthResponse: Gateways grouped by their health status.
        """
        url = self._build_url("health")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return GatewaysHealthResponse(**data)
