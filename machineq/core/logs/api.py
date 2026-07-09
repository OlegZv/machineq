"""Logs API resources for sync and async clients."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.logs import AckFilter, ActivationFilter, LateFilter, LogInstance, MessageTypeFilter, StreamFilter
from machineq.core.logs.models import LogResponse
from machineq.core.utils import ensure_utc_and_str

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


DEFAULT_PER_PAGE = 100


def populate_params(
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
) -> dict[str, str]:
    params: dict[str, str] = {}
    if deveui:
        params["DevEUI"] = deveui
    if gateway_id:
        params["GatewayID"] = gateway_id
    if start_time:
        params["StartTime"] = ensure_utc_and_str(start_time)
    if end_time:
        params["EndTime"] = ensure_utc_and_str(end_time)
    if page is not None:
        params["Page"] = str(page)
    if stream:
        params["LogFrameFilter.Stream"] = stream.value
    if message_type:
        params["LogFrameFilter.MessageType"] = message_type.value
    if late:
        params["LogFrameFilter.Late"] = late.value
    if activation:
        params["LogFrameFilter.Activation"] = activation.value
    if ack:
        params["LogFrameFilter.Ack"] = ack.value
    return params


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
        all_pages: bool = True,
    ) -> list[LogInstance]:
        """List logs with optional filtering.

        Args:
            deveui: Optional device EUI to filter by.
            gateway_id: Optional gateway ID to filter by.
            start_time: Optional ISO 8601 formatted start time.
            end_time: Optional ISO 8601 formatted end time.
            page: Optional page number for pagination.
            stream: Optional stream filter for log frames.
            message_type: Optional message type filter.
            late: Optional late flag filter.
            activation: Optional activation flag filter.
            ack: Optional acknowledgment flag filter.
            all_pages: Whether to pull all logs for the specified time period.

            Note: without specifying `page` or `all_ages` the API will return only 1 page (100 records).
            If the `page` is provided, the `all_pages` is ignored.

        Returns:
            LogResponse: Filtered logs matching the specified criteria.
        """
        params = populate_params(
            deveui, gateway_id, start_time, end_time, page, stream, message_type, late, activation, ack
        )
        if page is not None or not all_pages:
            # pulling either a specific page, or just a default "last" page (since all_pages is False)
            return self._get_single_page(params)

        # pull all pages
        all_logs: list[LogInstance] = []
        params["Page"] = "1"
        while new_page := self._get_single_page(params):
            all_logs.extend(new_page)
            if len(new_page) != DEFAULT_PER_PAGE:
                # less than expected records per page means no more pages left
                break
            params["Page"] = str(int(params["Page"]) + 1)
        return all_logs

    def _get_single_page(self, params: dict[str, str]) -> list[LogInstance]:
        response = self.client.http_client.get(
            self._build_url(),
            params=params,
            headers=self._build_headers(),
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
        all_pages: bool = True,
    ) -> list[LogInstance]:
        """List logs with optional filtering.

        Args:
            deveui: Optional device EUI to filter by.
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
            list[LogInstance]: Filtered logs matching the specified criteria.
        """
        params = populate_params(
            deveui, gateway_id, start_time, end_time, page, stream, message_type, late, activation, ack
        )
        if page is not None or not all_pages:
            # pulling either a specific page, or just a default "last" page (since all_pages is False)
            return await self._get_single_page(params)
        # pull all pages
        all_logs: list[LogInstance] = []
        params["Page"] = "1"

        # unfortunately the API doesn't tell us how many pages there are, so we
        # need to pull until we get less than DEFAULT_PER_PAGE sequentially
        while new_page := await self._get_single_page(params):
            all_logs.extend(new_page)
            if len(new_page) != DEFAULT_PER_PAGE:
                # less than expected records per page means no more pages left
                break
            params["Page"] = str(int(params["Page"]) + 1)
        return all_logs

    async def _get_single_page(self, params: dict[str, str]) -> list[LogInstance]:
        response = await self.client.http_client.get(
            self._build_url(),
            params=params,
            headers=self._build_headers(),
        )
        data = self._parse_response(response)
        return LogResponse(**data).logs
