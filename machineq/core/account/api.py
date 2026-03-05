"""Account API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.account.models import (
    AccountPermissionResponse,
    AccountResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncAccount(BaseResource["SyncClient"]):
    """Account resource for user account operations."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/account")

    def get(self) -> AccountResponse:
        """Retrieve the current user's account information.

        Returns:
            AccountResponse: The current user's account details.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return AccountResponse(**data)

    def get_permissions(self) -> AccountPermissionResponse:
        """Retrieve the current user's permissions.

        Returns:
            AccountPermissionResponse: The current user's permission details.
        """
        url = self._build_url("permissions")
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return AccountPermissionResponse(**data)


class AsyncAccount(BaseResource["AsyncClient"]):
    """Async account resource for user account operations."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/account")

    async def get(self) -> AccountResponse:
        """Retrieve the current user's account information.

        Returns:
            AccountResponse: The current user's account details.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return AccountResponse(**data)

    async def get_permissions(self) -> AccountPermissionResponse:
        """Retrieve the current user's permissions.

        Returns:
            AccountPermissionResponse: The current user's permission details.
        """
        url = self._build_url("permissions")
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return AccountPermissionResponse(**data)
