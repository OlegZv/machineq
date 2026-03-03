"""Pytest configuration and shared fixtures."""

import inspect
from functools import wraps
from os import getenv

import pytest
from dotenv import load_dotenv

from machineq import MqAuth
from machineq.client import AsyncClient, SyncClient

# Load environment variables from .env file
load_dotenv()


def sync_to_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def wrap_sync_nested(obj):
    """Wrap sync methods on nested objects (e.g. .account, .devices) to return awaitables."""
    for attr_name in dir(obj):
        if attr_name.startswith("_") or attr_name in ["auth", "http_client"]:
            continue
        attr = getattr(obj, attr_name)
        # Only wrap if it's an object with methods (like account, devices)
        if (
            not callable(attr)
            and not inspect.isclass(attr)
            and hasattr(attr, "__dict__")
            and not attr_name.startswith("_")
        ):
            for method_name in dir(attr):
                method = getattr(attr, method_name)
                if callable(method) and not inspect.iscoroutinefunction(method) and not method_name.startswith("_"):
                    setattr(attr, method_name, sync_to_async(method))
    return obj


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
def sync_client(auth_instance) -> SyncClient:
    """Get an authenticated sync client."""
    c = SyncClient("", "")
    c.auth = auth_instance
    return c


@pytest.fixture(scope="function")
def async_client(auth_instance) -> AsyncClient:
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
def client(request, sync_client, async_client):
    """Return a client sync and async. Sync is wrapped so that its methods can always be awaited.

    The fixture is parameterized so that every test runs twice: once with the
    synchronous client and once with the asynchronous one.  The wrapper hides the
    distinction from the test bodies.

    This way we can run the same test against both clients without having to duplicate
    the test code or sprinkle conditionals throughout the tests.
    """
    if request.param == "sync":
        return wrap_sync_nested(sync_client)
    else:
        return async_client


@pytest.fixture(scope="session")
def all_service_profiles(auth_instance):
    """Return the full list of service profiles (cached for the session)."""
    client = SyncClient("", "")
    client.auth = auth_instance
    profiles = client.service_profiles.get_all()
    assert profiles, "no service profiles available in the environment"
    return profiles


@pytest.fixture(scope="session")
def all_device_profiles(auth_instance):
    """Return the full list of device profiles (cached for the session)."""
    client = SyncClient("", "")
    client.auth = auth_instance
    profiles = client.device_profiles.get_all()
    assert profiles, "no device profiles available in the environment"
    return profiles


@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
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
