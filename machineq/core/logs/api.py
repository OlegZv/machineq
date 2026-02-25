"""Logs API resources for sync and async clients."""

from __future__ import annotations

import warnings
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.logs import AckFilter, ActivationFilter, LateFilter, LogInstance, MessageTypeFilter, StreamFilter
from machineq.core.logs.models import LogResponse

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


def ensure_utc_and_str(dt: datetime) -> str:
    """Ensure a datetime is timezone-aware in timezone.utc.
    If the user provides a naive datetime, issue a warning and try our best to convert from local
    timezone to timezone.utc. If the user provides a timezone-aware datetime, convert it to timezone.utc if it's not already.
    """
    if dt.tzinfo is None:
        # Naive datetime, assume it's in local timezone and convert to timezone.utc

        warnings.warn(
            "Naive datetime provided. Assuming local timezone and converting to timezone.utc. "
            "Please provide timezone-aware datetimes in the future.",
            UserWarning,
            stacklevel=2,
        )
        dt = dt.astimezone(timezone.utc)
    else:
        # Timezone-aware datetime, convert to timezone.utc if it's not already
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


class SyncLogs(BaseResource["SyncClient"]):
    """Logs resource for device and gateway message logs."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/logs")

    # ruff: noqa: C901
    def get_all(
        self,
        deveui: str | None = None,
        gateway_id: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        page: int | None = None,
        stream: StreamFilter | None = None,
        message_type: MessageTypeFilter | None = None,
        late: LateFilter | None = None,
        activation: ActivationFilter | None = None,
        ack: AckFilter | None = None,
    ) -> list[LogInstance]:
        """List logs with optional filtering.

        Args:
            device_eui: Optional device EUI to filter by.
            gateway_id: Optional gateway ID to filter by.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.
            page: Optional page number for pagination.
            stream: Optional stream filter for log frames.
            message_type: Optional message type filter.
            late: Optional late flag filter.
            activation: Optional activation flag filter.
            ack: Optional acknowledgment flag filter.

        Returns:
            LogResponse: Filtered logs matching the specified criteria.
        """
        url = self._build_url()
        params = {}
        if deveui:
            params["DevEUI"] = deveui
        if gateway_id:
            params["GatewayID"] = gateway_id
        if start_time:
            params["StartTime"] = ensure_utc_and_str(start_time)
        if end_time:
            params["EndTime"] = ensure_utc_and_str(end_time)
        if page is not None:
            params["Page"] = page
        if stream:
            params["LogFrameFilter.Stream"] = stream
        if message_type:
            params["LogFrameFilter.MessageType"] = message_type
        if late:
            params["LogFrameFilter.Late"] = late
        if activation:
            params["LogFrameFilter.Activation"] = activation
        if ack:
            params["LogFrameFilter.Ack"] = ack

        response = self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return LogResponse(**data).logs


class AsyncLogs(BaseResource["AsyncClient"]):
    """Async logs resource for device and gateway message logs."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/logs")

    # ruff: noqa: C901
    async def get_all(
        self,
        device_eui: str | None = None,
        gateway_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        page: int | None = None,
        stream: str | None = None,
        message_type: str | None = None,
        late: str | None = None,
        activation: str | None = None,
        ack: str | None = None,
    ) -> LogResponse:
        """List logs with optional filtering.

        Args:
            device_eui: Optional device EUI to filter by.
            gateway_id: Optional gateway ID to filter by.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.
            page: Optional page number for pagination.
            stream: Optional stream filter for log frames.
            message_type: Optional message type filter.
            late: Optional late flag filter.
            activation: Optional activation flag filter.
            ack: Optional acknowledgment flag filter.

        Returns:
            LogResponse: Filtered logs matching the specified criteria.
        """
        url = self._build_url()
        params = {}
        if device_eui:
            params["DevEUI"] = device_eui
        if gateway_id:
            params["GatewayID"] = gateway_id
        if start_time:
            params["StartTime"] = start_time
        if end_time:
            params["EndTime"] = end_time
        if page is not None:
            params["Page"] = page
        if stream:
            params["LogFrameFilter.Stream"] = stream
        if message_type:
            params["LogFrameFilter.MessageType"] = message_type
        if late:
            params["LogFrameFilter.Late"] = late
        if activation:
            params["LogFrameFilter.Activation"] = activation
        if ack:
            params["LogFrameFilter.Ack"] = ack

        response = await self.client.http_client.get(
            url,
            params=params,
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return LogResponse(**data)
