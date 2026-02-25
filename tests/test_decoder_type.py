"""Tests for Decoder Type API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.decoder_type.api import SyncDecoderTypes


@pytest.fixture
def decoder_types_api(sync_client: SyncClient) -> SyncDecoderTypes:
    """Get decoder types API resource."""
    return sync_client.decoder_types


class TestDecoderTypes:
    """Decoder Type API tests."""

    def test_get_all(self, decoder_types_api: SyncDecoderTypes):
        """Test listing all decoder types."""
        result = decoder_types_api.get_all()
        assert len(result) > 0
        assert result[0].id
        assert result[0].name
        assert result[0].payload_decoder

    def test_get_existing(self, decoder_types_api: SyncDecoderTypes):
        """Test retrieving a specific decoder type."""
        all_types = decoder_types_api.get_all()
        if all_types:
            dtype_id = all_types[0].id
            result = decoder_types_api.get(dtype_id)
            assert result.id == dtype_id
