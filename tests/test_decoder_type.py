"""Tests for Decoder Type API."""

import pytest


@pytest.mark.asyncio
class TestDecoderTypes:
    """Decoder Type API tests."""

    async def test_get_all(self, client):
        """Test listing all decoder types."""
        result = await client.decoder_types.get_all()
        assert len(result) > 0
        assert result[0].id
        assert result[0].name
        assert result[0].payload_decoder

    async def test_get_existing(self, client):
        """Test retrieving a specific decoder type."""
        all_types = await client.decoder_types.get_all()
        if all_types:
            dtype_id = all_types[0].id
            result = await client.decoder_types.get(dtype_id)
            assert result.id == dtype_id
