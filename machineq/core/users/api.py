"""User API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.users.models import (
    UserCreate,
    UserCreateResponse,
    UserInstance,
    UserPatch,
    UserResponse,
    UserUpdate,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncUsers(BaseResource["SyncClient"]):
    """Users resource for user account management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/users")

    def get_all(self) -> list[UserInstance]:
        """List all users.

        Returns:
            list[UserInstance]: List of all user instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return UserResponse(**data).users

    def get(self, user_id: str) -> UserInstance:
        """Retrieve a user by their ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            UserInstance: The user instance matching the given ID.
        """
        url = self._build_url(f"{user_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return UserInstance(**data)

    def create(self, data: UserCreate) -> str:
        """Create a new user.

        Args:
            data: The user creation data.

        Returns:
            str: The ID of the newly created user.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserCreateResponse(**result).id

    def update(self, user_id: str, data: UserUpdate) -> UserInstance:
        """Update a user (full replacement).

        Args:
            user_id: The unique identifier of the user.
            data: The complete user data for replacement.

        Returns:
            UserInstance: The updated user instance.
        """
        url = self._build_url(f"{user_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserInstance(**result)

    def patch(self, user_id: str, data: UserPatch) -> UserInstance:
        """Partially update a user.

        Args:
            user_id: The unique identifier of the user.
            data: The partial user data to update.

        Returns:
            UserInstance: The updated user instance.
        """
        url = self._build_url(f"{user_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserInstance(**result)

    def delete(self, user_id: str) -> None:
        """Delete a user.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            None
        """
        url = self._build_url(f"{user_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)


class AsyncUsers(BaseResource["AsyncClient"]):
    """Async users resource for user account management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/users")

    async def get_all(self) -> list[UserInstance]:
        """List all users.

        Returns:
            list[UserInstance]: List of all user instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return UserResponse(**data).users

    async def get(self, user_id: str) -> UserInstance:
        """Retrieve a user by their ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            UserInstance: The user instance matching the given ID.
        """
        url = self._build_url(f"{user_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return UserInstance(**data)

    async def create(self, data: UserCreate) -> str:
        """Create a new user.

        Args:
            data: The user creation data.

        Returns:
            str: The ID of the newly created user.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserCreateResponse(**result).id

    async def update(self, user_id: str, data: UserUpdate) -> UserInstance:
        """Update a user (full replacement).

        Args:
            user_id: The unique identifier of the user.
            data: The complete user data for replacement.

        Returns:
            UserInstance: The updated user instance.
        """
        url = self._build_url(f"{user_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserInstance(**result)

    async def patch(self, user_id: str, data: UserPatch) -> UserInstance:
        """Partially update a user.

        Args:
            user_id: The unique identifier of the user.
            data: The partial user data to update.

        Returns:
            UserInstance: The updated user instance.
        """
        url = self._build_url(f"{user_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return UserInstance(**result)

    async def delete(self, user_id: str) -> None:
        """Delete a user.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            None
        """
        url = self._build_url(f"{user_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)
