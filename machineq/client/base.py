"""Base resource class for API resources."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import httpx
from pydantic import BaseModel

from machineq import MqApiEnvironment

from .exceptions import parse_error_response

if TYPE_CHECKING:
    from .async_ import AsyncClient
    from .sync import SyncClient

ClientType = TypeVar("ClientType", "SyncClient", "AsyncClient")


class BaseResource(Generic[ClientType]):
    """Base class for API resources."""

    def __init__(
        self,
        client: ClientType,
        base_path: str,
        version: str | None = None,
    ):
        """Initialize resource.

        Args:
            client: Parent client instance (sync or async)
            base_path: Base path for this resource (e.g., '/devices')
        """
        self.client: ClientType = client
        # if version is provided, use it; otherwise, inherit from client
        if version is not None:
            self.version = version
        else:
            self.version = client.api_version
        self.extra_prefix = client.extra_prefix
        self.base_path = base_path

    def get_all_generic(self: BaseResource[SyncClient]) -> Any:  # noqa: ANN401
        """Common function for get_all, returns parsed json"""
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return data

    async def get_all_generic_async(self: BaseResource[AsyncClient]) -> Any:  # noqa: ANN401
        """Common function for get_all, returns parsed json"""
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers())
        data = self._parse_response(response)
        return data

    @property
    def base_url(self) -> str:
        """Construct base URL for this resource."""
        env = "" if self.client.auth.env == MqApiEnvironment.PROD else f"{self.client.auth.env}."
        return f"https://api.{env}machineq.net/{self.version}{self.extra_prefix}"

    def _build_url(self, path: str = "") -> str:
        """Build full URL for a request.

        Args:
            path: Relative path (can include format params like {id})

        Returns:
            Full URL
        """
        if path.startswith("/"):
            return f"{self.base_url}{path}"
        if path:
            return f"{self.base_url}{self.base_path}/{path}"
        return f"{self.base_url}{self.base_path}"

    # the actual return type for this call is None | list | dict | str
    # but then subsequent calls to try and serialize it, like SomeModel(**data)
    # fail type check, since it can only do that with a dict. Long term a better
    # way would be to possibly pass a type instance and return that type instance.
    @staticmethod
    def _parse_response(response: httpx.Response) -> Any:  # noqa: ANN401
        """Parse JSON response.

        Args:
            response: httpx response

        Returns:
            Parsed JSON or None if empty

        Raises:
            APIError: If response is not successful
        """
        # Check for success first
        if not response.is_success:
            try:
                data = response.json()
            except (json.JSONDecodeError, ValueError):
                # Response is not JSON, create generic error
                data = {
                    "message": response.text or f"HTTP {response.status_code}",
                    "code": response.status_code,
                }

            raise parse_error_response(data, status_code=response.status_code)

        # Empty success response (e.g., 204 No Content)
        if not response.content:
            return None

        # Parse successful JSON response
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            # If no content, return None
            if not response.text:
                return None
            # If we can't parse, return text
            return response.text

    def _build_headers(self) -> dict[str, str]:
        """Build request headers with auth token.
        Returns:
            Headers dict with Authorization header
        """
        return {
            "Authorization": f"Bearer {self.client.auth.token}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _serialize_request_data(data: BaseModel | dict) -> str:
        """Serialize request data to JSON.

        Args:
            data: Data to serialize (Pydantic model, dict, etc.)

        Returns:
            JSON string
        """

        # Handle Pydantic models: serialize with by_alias to use API PascalCase
        if isinstance(data, BaseModel):
            return data.model_dump_json(by_alias=True, exclude_none=True)

        # Handle dicts
        if isinstance(data, dict):
            return json.dumps(data)

        # Fallback
        return json.dumps(data)
