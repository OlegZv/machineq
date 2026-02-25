"""Output Profile API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.output_profile.models import (
    OutputProfileCreate,
    OutputProfileCreateResponse,
    OutputProfileDevicesResponse,
    OutputProfileDevicesUpdate,
    OutputProfileDevicesUpdateResponse,
    OutputProfileInstance,
    OutputProfilePatch,
    OutputProfileResponse,
    OutputProfileUpdate,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncOutputProfiles(BaseResource["SyncClient"]):
    """Output profiles resource for data routing profiles."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/outputprofiles")

    def get_all(self) -> list[OutputProfileInstance]:
        """List all output profiles.

        Returns:
            list[OutputProfileInstance]: List of all output profile instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileResponse(**data).output_profiles

    def get(self, profile_id: str) -> OutputProfileInstance:
        """Retrieve an output profile by its ID.

        Args:
            profile_id: The unique identifier of the output profile.

        Returns:
            OutputProfileInstance: The output profile instance matching the given ID.
        """
        url = self._build_url(f"{profile_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileInstance(**data)

    def create(self, data: OutputProfileCreate) -> str:
        """Create a new output profile.

        Args:
            data: The output profile creation data.

        Returns:
            str: The ID of the newly created output profile.
        """
        url = self._build_url()
        response = self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileCreateResponse(**result).id

    def update(
        self,
        profile_id: str,
        data: OutputProfileUpdate,
    ) -> OutputProfileInstance:
        """Update an output profile (full replacement).

        Args:
            profile_id: The unique identifier of the output profile.
            data: The complete output profile data for replacement.

        Returns:
            OutputProfileInstance: The updated output profile instance.
        """
        url = self._build_url(f"{profile_id}")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileInstance(**result)

    def patch(
        self,
        profile_id: str,
        data: OutputProfilePatch,
    ) -> OutputProfileInstance:
        """Partially update an output profile.

        Args:
            profile_id: The unique identifier of the output profile.
            data: The partial output profile data to update.

        Returns:
            OutputProfileInstance: The updated output profile instance.
        """
        url = self._build_url(f"{profile_id}")
        response = self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileInstance(**result)

    def delete(self, profile_id: str) -> None:
        """Delete an output profile.

        Args:
            profile_id: The unique identifier of the output profile to delete.

        Returns:
            None
        """
        url = self._build_url(f"{profile_id}")
        response = self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    def get_devices(self, profile_id: str):
        """Retrieve devices associated with an output profile.

        Args:
            profile_id: The unique identifier of the output profile.

        Returns:
            OutputProfileDevicesResponse: Devices associated with the output profile.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileDevicesResponse(**data)

    def update_devices(
        self,
        profile_id: str,
        data: OutputProfileDevicesUpdate,
    ) -> OutputProfileDevicesUpdateResponse:
        """Update devices associated with an output profile.

        Args:
            profile_id: The unique identifier of the output profile.
            data: The device association update data.

        Returns:
            OutputProfileDevicesUpdateResponse: The response containing updated device associations.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileDevicesUpdateResponse(**result)


class AsyncOutputProfiles(BaseResource["AsyncClient"]):
    """Async output profiles resource for data routing profiles."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/outputprofiles")

    async def get_all(self) -> list[OutputProfileInstance]:
        """List all output profiles.

        Returns:
            list[OutputProfileInstance]: List of all output profile instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileResponse(**data).output_profiles

    async def get(self, profile_id: str) -> OutputProfileInstance:
        """Retrieve an output profile by its ID.

        Args:
            profile_id: The unique identifier of the output profile.

        Returns:
            OutputProfileInstance: The output profile instance matching the given ID.
        """
        url = self._build_url(f"{profile_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileInstance(**data)

    async def create(self, data: OutputProfileCreate) -> str:
        """Create a new output profile.

        Args:
            data: The output profile creation data.

        Returns:
            str: The ID of the newly created output profile.
        """
        url = self._build_url()
        response = await self.client.http_client.post(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileCreateResponse(**result).id

    async def update(
        self,
        profile_id: str,
        data: OutputProfileUpdate,
    ) -> OutputProfileInstance:
        """Update an output profile (full replacement).

        Args:
            profile_id: The unique identifier of the output profile.
            data: The complete output profile data for replacement.

        Returns:
            OutputProfileInstance: The updated output profile instance.
        """
        url = self._build_url(f"{profile_id}")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileInstance(**result)

    async def patch(
        self,
        profile_id: str,
        data: OutputProfilePatch,
    ) -> OutputProfileInstance:
        """Partially update an output profile.

        Args:
            profile_id: The unique identifier of the output profile.
            data: The partial output profile data to update.

        Returns:
            OutputProfileInstance: The updated output profile instance.
        """
        url = self._build_url(f"{profile_id}")
        response = await self.client.http_client.patch(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileInstance(**result)

    async def delete(self, profile_id: str) -> None:
        """Delete an output profile.

        Args:
            profile_id: The unique identifier of the output profile to delete.

        Returns:
            None
        """
        url = self._build_url(f"{profile_id}")
        response = await self.client.http_client.delete(url, headers=self._build_headers(self.auth))
        self._parse_response(response)

    async def get_devices(self, profile_id: str):
        """Retrieve devices associated with an output profile.

        Args:
            profile_id: The unique identifier of the output profile.

        Returns:
            OutputProfileDevicesResponse: Devices associated with the output profile.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return OutputProfileDevicesResponse(**data)

    async def update_devices(
        self,
        profile_id: str,
        data: OutputProfileDevicesUpdate,
    ) -> OutputProfileDevicesUpdateResponse:
        """Update devices associated with an output profile.

        Args:
            profile_id: The unique identifier of the output profile.
            data: The device association update data.

        Returns:
            OutputProfileDevicesUpdateResponse: The response containing updated device associations.
        """
        url = self._build_url(f"{profile_id}/devices")
        response = await self.client.http_client.put(
            url,
            content=self._serialize_request_data(data),
            headers=self._build_headers(self.auth),
        )
        result = self._parse_response(response)
        return OutputProfileDevicesUpdateResponse(**result)
