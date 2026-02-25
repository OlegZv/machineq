"""Account API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.account.models import (
    AccountPasswordReset,
    AccountPermissionResponse,
    AccountResponse,
    UserInfoPatch,
    UserInfoUpdate,
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
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return AccountResponse(**data)

    def get_permissions(self) -> AccountPermissionResponse:
        """Retrieve the current user's permissions.

        Returns:
            AccountPermissionResponse: The current user's permission details.
        """
        url = self._build_url("permissions")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return AccountPermissionResponse(**data)

    def patch_user_info(self, data: UserInfoPatch) -> AccountResponse:
        """Partially update the current user's information.

        Args:
            data: Partial user information to update.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("patchUserInfo")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)

    def update_user_info(self, data: UserInfoUpdate) -> AccountResponse:
        """Update the current user's full information.

        Args:
            data: Complete user information for replacement.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("updateUserInfo")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)

    def password_reset(self, data: AccountPasswordReset) -> AccountResponse:
        """Change the current user's password.

        Args:
            data: Password reset data containing old and new passwords.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("passwordReset")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)


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
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return AccountResponse(**data)

    async def get_permissions(self) -> AccountPermissionResponse:
        """Retrieve the current user's permissions.

        Returns:
            AccountPermissionResponse: The current user's permission details.
        """
        url = self._build_url("permissions")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return AccountPermissionResponse(**data)

    async def patch_user_info(self, data: UserInfoPatch) -> AccountResponse:
        """Partially update the current user's information.

        Args:
            data: Partial user information to update.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("patchUserInfo")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)

    async def update_user_info(self, data: UserInfoUpdate) -> AccountResponse:
        """Update the current user's full information.

        Args:
            data: Complete user information for replacement.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("updateUserInfo")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)

    async def password_reset(self, data: AccountPasswordReset) -> AccountResponse:
        """Change the current user's password.

        Args:
            data: Password reset data containing old and new passwords.

        Returns:
            AccountResponse: The updated account information.
        """
        url = self._build_url("passwordReset")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return AccountResponse(**result)
