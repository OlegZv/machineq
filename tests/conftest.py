"""Pytest configuration and shared fixtures."""

from os import getenv
from typing import Protocol

import pytest
from dotenv import load_dotenv

from machineq import MqAuth
from machineq.client import AsyncClient, SyncClient
from machineq.core.device_profile import DeviceProfileInstance
from machineq.core.service_profile import ServiceProfileInstance
from tests.async_test_client import AsyncTestClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def auth_instance() -> MqAuth:
    """Get an authenticated MqAuth instance."""
    client_id = getenv("MQ_CLIENT_ID")
    client_secret = getenv("MQ_CLIENT_SECRET")
    assert client_id is not None, "MQ_CLIENT_ID must be set in environment"
    assert client_secret is not None, "MQ_CLIENT_SECRET must be set in environment"
    auth = MqAuth(client_id, client_secret)
    auth.refresh()
    return auth


@pytest.fixture(scope="session")
def sync_client(auth_instance: MqAuth) -> SyncClient:
    """Get an authenticated sync client."""
    c = SyncClient("", "")
    c.auth = auth_instance
    return c


@pytest.fixture(scope="function")
def async_client(auth_instance: MqAuth) -> AsyncClient:
    """Get an authenticated async client. There may be a better way to share the client across tests, but
    the reason it's function-scopes is because the httpx library connection pool management may result in
    multiple nested couroutines (pytest + httpx). This could lead to event loop closing in one test and
    while being used in anoher test. This leads to `RuntimeError: Event loop is closed` errors.
    Making client function-scoped ensures a fresh client (and event loop) for each test, avoiding these issues.

    We still reuse the auth_instance to avoid grabbing he token multiple times for each test.
    https://docs.aiohttp.org/en/stable/http_request_lifecycle.html#aiohttp-request-lifecycle
    """
    c = AsyncClient("", "")
    c.auth = auth_instance
    return c


@pytest.fixture(scope="function", params=["sync", "async"], ids=["sync", "async"])
def client(request: pytest.FixtureRequest, sync_client: SyncClient, async_client: AsyncClient) -> AsyncTestClient:
    """Return an AsyncTestClient for sync and async testing.

    The fixture is parameterized so that every test runs twice: once with the
    synchronous client and once with the asynchronous one.  The wrapper hides the
    distinction from the test bodies.

    This way we can run the same test against both clients without having to duplicate
    the test code or sprinkle conditionals throughout the tests.
    """
    if request.param == "sync":
        return AsyncTestClient(sync_client)
    else:
        return AsyncTestClient(async_client)


@pytest.fixture(scope="session")
def all_service_profiles(auth_instance: MqAuth) -> list[ServiceProfileInstance]:
    """Return the full list of service profiles (cached for the session)."""
    client = SyncClient("", "")
    client.auth = auth_instance
    profiles = client.service_profiles.get_all()
    assert len(profiles) > 0, "no service profiles available in the environment"
    return profiles


@pytest.fixture(scope="session")
def all_device_profiles(auth_instance: MqAuth) -> list[DeviceProfileInstance]:
    """Return the full list of device profiles (cached for the session)."""
    client = SyncClient("", "")
    client.auth = auth_instance
    profiles = client.device_profiles.get_all()
    assert profiles, "no device profiles available in the environment"
    return profiles


class ProfileGetter(Protocol):
    def __call__(self, exclude: list[str] | None = None) -> str: ...


@pytest.fixture(scope="function")
def get_service_profile(all_service_profiles: list[ServiceProfileInstance]) -> ProfileGetter:
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


@pytest.fixture(scope="function")
def get_device_profile(all_device_profiles: list[DeviceProfileInstance]) -> ProfileGetter:
    """Return a device profile ID, optionally excluding some.

    See :func:`get_service_profile` for details.
    """

    def _selector(exclude: list[str] | None = None) -> str:
        for p in all_device_profiles:
            if not exclude or p.id not in exclude:
                return p.id
        pytest.skip("no device profile available after exclusions")

    return _selector
