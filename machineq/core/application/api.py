"""Application API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.application import ApplicationCreateResponse
from machineq.core.application.models import (
    ApplicationCreate,
    ApplicationInstance,
    ApplicationPatch,
    ApplicationResponse,
    ApplicationUpdate,
    RefreshApplicationResponse,
)
from machineq.core.shared.models import CommonOKResponse

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncApplications(BaseResource["SyncClient"]):
    """Applications resource for OAuth application management."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/applications")

    def get_all(self) -> list[ApplicationInstance]:
        """List all applications.

        Returns:
            list[ApplicationInstance]: List of all application instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ApplicationResponse(**data).applications

    def get(self, application_id: str) -> ApplicationInstance:
        """Retrieve an application by its ID.

        Args:
            application_id: The unique identifier of the application.

        Returns:
            ApplicationInstance: The application instance matching the given ID.
        """
        url = self._build_url(f"{application_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ApplicationInstance(**data)

    def create(self, data: ApplicationCreate) -> ApplicationCreateResponse:
        """Create a new application.

        Args:
            data: The application creation data.

        Returns:
            str: The ID of the newly created application.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return ApplicationCreateResponse(**result)

    def update(self, application_id: str, data: ApplicationUpdate) -> bool:
        """Update an application (full replacement).

        Args:
            application_id: The unique identifier of the application.
            data: The complete application data for replacement.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        url = self._build_url(f"{application_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def patch(self, application_id: str, data: ApplicationPatch) -> bool:
        """Partially update an application.

        Args:
            application_id: The unique identifier of the application.
            data: The partial application data to update.

        Returns:
            bool: True if the patch was successful, False otherwise.
        """
        url = self._build_url(f"{application_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return CommonOKResponse(**result).response

    def delete(self, application_id: str) -> None:
        """Delete an application.

        Args:
            application_id: The unique identifier of the application to delete.

        Returns:
            None
        """
        url = self._build_url(f"{application_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    def refresh_token(self, application_id: str) -> str:
        """Refresh the application's token.

        Args:
            application_id: The unique identifier of the application.

        Returns:
            str: The new client secret.
        """
        url = self._build_url(f"{application_id}/refreshToken")
        response = self.client.http_client.post(
            url,
            content="{}",
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return RefreshApplicationResponse(**data).client_secret


class AsyncApplications(BaseResource["AsyncClient"]):
    """Async applications resource for OAuth application management."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/applications")

    async def get_all(self) -> list[ApplicationInstance]:
        """List all applications.

        Returns:
            list[ApplicationInstance]: List of all application instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ApplicationResponse(**data).applications

    async def get(self, application_id: str) -> ApplicationInstance:
        """Retrieve an application by its ID.

        Args:
            application_id: The unique identifier of the application.

        Returns:
            ApplicationInstance: The application instance matching the given ID.
        """
        url = self._build_url(f"{application_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return ApplicationInstance(**data)

    async def create(self, data: ApplicationCreate) -> str:
        """Create a new application.

        Args:
            data: The application creation data.

        Returns:
            str: The ID of the newly created application.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return ApplicationInstance(**result).id

    async def update(self, application_id: str, data: ApplicationUpdate) -> ApplicationInstance:
        """Update an application (full replacement).

        Args:
            application_id: The unique identifier of the application.
            data: The complete application data for replacement.

        Returns:
            ApplicationInstance: The updated application instance.
        """
        url = self._build_url(f"{application_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return ApplicationInstance(**result)

    async def patch(self, application_id: str, data: ApplicationPatch) -> ApplicationInstance:
        """Partially update an application.

        Args:
            application_id: The unique identifier of the application.
            data: The partial application data to update.

        Returns:
            ApplicationInstance: The updated application instance.
        """
        url = self._build_url(f"{application_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return ApplicationInstance(**result)

    async def delete(self, application_id: str) -> None:
        """Delete an application.

        Args:
            application_id: The unique identifier of the application to delete.

        Returns:
            None
        """
        url = self._build_url(f"{application_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    async def refresh_token(self, application_id: str) -> RefreshApplicationResponse:
        """Refresh the application's token.

        Args:
            application_id: The unique identifier of the application.

        Returns:
            RefreshApplicationResponse: The new token and related information.
        """
        url = self._build_url(f"{application_id}/refreshToken")
        response = await self.client.http_client.post(
            url,
            content="{}",
            headers=self._build_headers(self.auth),
        )
        data = self._parse_response(response)
        return RefreshApplicationResponse(**data)
