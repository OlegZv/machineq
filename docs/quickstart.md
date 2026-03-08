# Quickstart

This page shows how to install the library and make your first calls using both the **synchronous**
and **asynchronous** clients.

## Installation

Use `uv` (recommended for local development of this repository), to add it to your project with:

```bash
uv add machineq
```

Or using `pip`
```bash
pip install machineq
```

## Authentication and environments

MachineQ uses OAuth2 client credentials. You will need:

- `client_id`
- `client_secret`

You can also choose which API environment to talk to, via [`MqApiEnvironment`][machineq.MqApiEnvironment]. By default,
the clients use the production environment.

```python
from machineq import MqApiEnvironment, SyncClient

client = SyncClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
)
```

## First request with the synchronous client

```python
from machineq import SyncClient

client = SyncClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
)

devices = client.devices.get_all()
print(devices)
```

You can also use the sync client as a context manager:

```python
from machineq import SyncClient

with SyncClient("your-client-id", "your-client-secret") as client:
    devices = client.devices.get_all()
    print(devices)
```

## First request with the asynchronous client

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

## Next steps

- Read the [Clients usage guide](usage/clients.md) for more details on sync vs async usage.
- Explore the [API Reference](api/client.md) for all available client methods and exceptions.
