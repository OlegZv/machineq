"""Decoder Type API resources for sync and async clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from machineq.client.base import BaseResource
from machineq.core.decoder_type.models import (
    DecoderTypeInstance,
    DecoderTypeResponse,
)

if TYPE_CHECKING:
    from machineq.client.async_ import AsyncClient
    from machineq.client.sync import SyncClient


class SyncDecoderTypes(BaseResource["SyncClient"]):
    """Decoder types resource for device payload decoders."""

    def __init__(self, client: SyncClient):
        super().__init__(client, "/decodertypes")

    def get_all(self) -> list[DecoderTypeInstance]:
        """List all available decoder types.

        Returns:
            list[DecoderTypeInstance]: List of all decoder type instances.
        """
        url = self._build_url()
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DecoderTypeResponse(**data).decoder_types

    def get(self, decoder_id: str) -> DecoderTypeInstance:
        """Retrieve a decoder type by its ID.

        Args:
            decoder_id: The unique identifier of the decoder type.

        Returns:
            DecoderTypeInstance: The decoder type instance matching the given ID.
        """
        url = self._build_url(f"{decoder_id}")
        response = self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DecoderTypeInstance(**data)


class AsyncDecoderTypes(BaseResource["AsyncClient"]):
    """Async decoder types resource for device payload decoders."""

    def __init__(self, client: AsyncClient):
        super().__init__(client, "/decodertypes")

    async def get_all(self) -> list[DecoderTypeInstance]:
        """List all available decoder types.

        Returns:
            list[DecoderTypeInstance]: List of all decoder type instances.
        """
        url = self._build_url()
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DecoderTypeResponse(**data).decoder_types

    async def get(self, decoder_id: str) -> DecoderTypeInstance:
        """Retrieve a decoder type by its ID.

        Args:
            decoder_id: The unique identifier of the decoder type.

        Returns:
            DecoderTypeInstance: The decoder type instance matching the given ID.
        """
        url = self._build_url(f"{decoder_id}")
        response = await self.client.http_client.get(url, headers=self._build_headers(self.auth))
        data = self._parse_response(response)
        return DecoderTypeInstance(**data)
