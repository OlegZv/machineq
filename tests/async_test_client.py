# tests/async_test_client.py
from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from types import CoroutineType, TracebackType
from typing import Any, TypeVar

from machineq.client import AsyncClient, SyncClient

T = TypeVar("T", SyncClient, AsyncClient)


def sync_to_async(func: Callable) -> CoroutineType:
    """Convert a sync function to an async one by wrapping it."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        return func(*args, **kwargs)

    return wrapper  # ty:ignore[invalid-return-type]


def wrap_sync_nested(obj: T) -> AsyncClient[T]:
    """Wrap sync methods on nested objects (e.g., .gateways) to return awaitables."""
    for attr_name in dir(obj):
        if attr_name.startswith("_") or attr_name in ["auth", "http_client"]:
            continue
        attr = getattr(obj, attr_name)
        # Only wrap if it's an object with methods (like gateways, devices)
        if (
            not callable(attr)
            and not inspect.isclass(attr)
            and hasattr(attr, "__dict__")
            and not attr_name.startswith("_")
        ):
            for method_name in dir(attr):
                method = getattr(attr, method_name)
                if callable(method) and not inspect.iscoroutinefunction(method) and not method_name.startswith("_"):
                    setattr(attr, method_name, sync_to_async(method))
    return obj


class AsyncTestClient:
    """A unified async test client that wraps either AsyncClient or SyncClient.

    This ensures all methods are async and provides clear typing for tests.
    """

    def __init__(self, client: AsyncClient | SyncClient):
        """Initialize with either an AsyncClient or SyncClient.

        If SyncClient is provided, its methods are wrapped to be async.
        """
        if isinstance(client, AsyncClient):
            self._client = client
        else:  # SyncClient
            # Wrap the sync client to make it async
            self._client = wrap_sync_nested(client)

        # Expose all attributes from the underlying client
        self.auth = self._client.auth
        self.api_version = self._client.api_version
        self.extra_prefix = self._client.extra_prefix
        self.http_client = self._client.http_client

        # Expose resource attributes (these will be async after wrapping if needed)
        self.account = self._client.account
        self.applications = self._client.applications
        self.decoder_types = self._client.decoder_types
        self.devices = self._client.devices
        self.device_groups = self._client.device_groups
        self.device_profiles = self._client.device_profiles
        self.gateways = self._client.gateways
        self.gateway_groups = self._client.gateway_groups
        self.gateway_profiles = self._client.gateway_profiles
        self.logs = self._client.logs
        self.multicast_groups = self._client.multicast_groups
        self.output_profiles = self._client.output_profiles
        self.rf_regions = self._client.rf_regions
        self.roles = self._client.roles
        self.service_profiles = self._client.service_profiles
        self.users = self._client.users
        self.version = self._client.version

    async def aclose(self) -> None:
        """Close the client (async for consistency)."""
        if hasattr(self._client, "aclose"):
            await self._client.aclose()
        else:
            self._client.close()

    async def __aenter__(self) -> AsyncTestClient:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.aclose()
