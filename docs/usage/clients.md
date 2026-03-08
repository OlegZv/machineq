# Clients usage

The library exposes two main client types:

- [`SyncClient`][machineq.SyncClient] for traditional blocking code.
- [`AsyncClient`][machineq.AsyncClient] for asynchronous calls.

Both expose the same set of resource groups (devices, gateways, users, etc.) so you can choose the
style that best fits your application.

## Synchronous client

```python
from machineq import SyncClient

client = SyncClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
)

devices = client.devices.get_all()
print(devices)
```

### Using the sync client as a context manager

The synchronous client wraps an `httpx.Client`. To make sure connections are properly closed, you
can use it as a context manager:

```python
from machineq import SyncClient

with SyncClient("your-client-id", "your-client-secret") as client:
    account = client.account.get()
    devices = client.devices.get_all()
    print(account, devices)
```

### Customizing version and URL prefix

The clients accept optional `version` and `extra_prefix` parameters that are combined with the
selected environment to build the base API URL.

```python
from machineq import MqApiEnvironment, SyncClient

client = SyncClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    version="v1",
    extra_prefix="",
    env=MqApiEnvironment.PROD,
)
```

Typically you can rely on the defaults, but these options are available if you need to adjust
routing for different deployments.

## Asynchronous client

```python
import asyncio

from machineq import AsyncClient


async def main() -> None:
    async with AsyncClient(
        client_id="your-client-id",
        client_secret="your-client-secret",
    ) as client:
        devices = await client.devices.get_all()
        print(devices)


asyncio.run(main())
```

Like the sync client, you can also construct `AsyncClient` without a context manager and call
`await client.aclose()` when you are done.

## Common resource patterns

Both clients expose the same resource groups as attributes. For example:

```python
from machineq import SyncClient

with SyncClient("your-client-id", "your-client-secret") as client:
    # Account information
    account = client.account.get()

    # Devices listing
    devices = client.devices.get_all()

    # Users
    users = client.users.get_all()

    print(account, devices, users)
```

For the async client the shape is the same, except that calls are `await`-able:

```python
from machineq import AsyncClient


async def list_devices(client: AsyncClient) -> None:
    devices = await client.devices.get_all()
    print(devices)
```

Refer to the [API Reference](../api/client.md) for full details on the available methods on each
resource.
