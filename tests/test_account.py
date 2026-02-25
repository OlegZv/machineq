"""Tests for Account API."""

import pytest

from machineq.client.sync import SyncClient
from machineq.core.account.api import SyncAccount


@pytest.fixture
def account_api(sync_client: SyncClient) -> SyncAccount:
    """Get account API resource."""
    return sync_client.account


class TestAccount:
    """Account API tests."""

    def test_get(self, account_api: SyncAccount):
        """Test getting account information."""
        result = account_api.get()
        assert result.subscriber_info
        assert result.subscriber_info.id
        assert result.subscriber_info.name
        assert result.subscriber_info.address
        assert result.subscriber_info.city
        assert result.subscriber_info.state
        assert result.subscriber_info.country
        assert result.subscriber_info.postal_code

    def test_get_permissions(self, account_api: SyncAccount):
        """Test getting permissions."""
        account_api.get_permissions()
        # if we were able to parse the data, it means the correct response was returned
