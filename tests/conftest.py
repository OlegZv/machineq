"""Pytest configuration and shared fixtures."""

from os import getenv

import pytest
from dotenv import load_dotenv

from machineq.client import SyncClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def sync_client() -> SyncClient:
    """Get an authenticated sync client."""
    client_id = getenv("MQ_CLIENT_ID")
    client_secret = getenv("MQ_CLIENT_SECRET")
    assert client_id is not None, "MQ_CLIENT_ID must be set in environment"
    assert client_secret is not None, "MQ_CLIENT_SECRET must be set in environment"
    return SyncClient(client_id, client_secret)


@pytest.fixture(scope="session")
def all_service_profiles(sync_client):
    """Return the full list of service profiles (cached for the session)."""
    profiles = sync_client.service_profiles.get_all()
    assert profiles, "no service profiles available in the environment"
    return profiles


@pytest.fixture(scope="session")
def all_device_profiles(sync_client):
    """Return the full list of device profiles (cached for the session)."""
    profiles = sync_client.device_profiles.get_all()
    assert profiles, "no device profiles available in the environment"
    return profiles


@pytest.fixture
def get_service_profile(all_service_profiles):
    """Return a service profile ID, optionally excluding some.

    The returned callable accepts an optional ``exclude`` list of IDs. If
    ``exclude`` filters out all candidates, the test is skipped rather than
    failing, since some environments only have a single profile.
    """

    def _selector(exclude: list[str] | None = None) -> str:
        for p in all_service_profiles:
            if not exclude or p.id not in exclude:
                return p.id
        pytest.skip("no service profile available after exclusions")

    return _selector


@pytest.fixture
def get_device_profile(all_device_profiles):
    """Return a device profile ID, optionally excluding some.

    See :func:`get_service_profile` for details.
    """

    def _selector(exclude: list[str] | None = None) -> str:
        for p in all_device_profiles:
            if not exclude or p.id not in exclude:
                return p.id
        pytest.skip("no device profile available after exclusions")

    return _selector
