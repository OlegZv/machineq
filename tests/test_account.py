"""Tests for Account API."""

import pytest
import pytest_asyncio

from machineq.core.account.api import AsyncAccount, SyncAccount


@pytest_asyncio.fixture
async def account_api(client) -> SyncAccount | AsyncAccount:
    """Get account API resource from whichever client is requested."""
    return client.account


@pytest.mark.asyncio
class TestAccount:
    """Account API tests."""

    async def test_get(self, account_api):
        """Test getting account information."""
        result = await account_api.get()
        assert result.subscriber_info
        assert result.subscriber_info.id
        assert result.subscriber_info.name
        assert result.subscriber_info.address
        assert result.subscriber_info.city
        assert result.subscriber_info.state
        assert result.subscriber_info.country
        assert result.subscriber_info.postal_code

    async def test_get_permissions(self, account_api):
        """Test getting permissions."""
        await account_api.get_permissions()
        # if we were able to parse the data, it means the correct response was returned
