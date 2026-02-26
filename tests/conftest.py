"""Pytest configuration and shared fixtures."""

from os import getenv

import pytest
from dotenv import load_dotenv

from machineq.client import SyncClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture
def sync_client() -> SyncClient:
    """Get an authenticated sync client."""
    client_id = getenv("MQ_CLIENT_ID")
    client_secret = getenv("MQ_CLIENT_SECRET")
    assert client_id is not None, "MQ_CLIENT_ID must be set in environment"
    assert client_secret is not None, "MQ_CLIENT_SECRET must be set in environment"
    return SyncClient(client_id, client_secret)
