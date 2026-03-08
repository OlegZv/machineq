<h1 align="center">MachineQ Python API Client</h1>

<p align="center">
  <a href="https://img.shields.io/github/v/release/OlegZv/machineq">
    <img src="https://img.shields.io/github/v/release/OlegZv/machineq" alt="Release" />
  </a>
  <a href="https://github.com/OlegZv/machineq/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/OlegZv/machineq/main.yml?branch=main&label=Build/Test/Lint" alt="Build/Test/Lint status" />
  </a>

  <a href="https://github.com/OlegZv/machineq/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/OlegZv/machineq/main.yml?branch=main" alt="Build status" />
  </a>
  <a href="https://codecov.io/gh/OlegZv/machineq">
    <img src="https://codecov.io/gh/OlegZv/machineq/branch/main/graph/badge.svg" alt="codecov" />
  </a>
  <a href="https://img.shields.io/github/commit-activity/m/OlegZv/machineq">
    <img src="https://img.shields.io/github/commit-activity/m/OlegZv/machineq" alt="Commit activity" />
  </a>
  <a href="https://img.shields.io/github/license/OlegZv/machineq">
    <img src="https://img.shields.io/github/license/OlegZv/machineq" alt="License" />
  </a>
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/machineq">

</p>

## Installation

Recommended installation using `uv add machineq` (or via pip" `pip install machineq`)

## Example Usage

For more examples and API reference check out [the quickstart section](https://machineq.readthedocs.io/en/latest/quickstart/) and [usage](https://machineq.readthedocs.io/en/latest/usage/clients/).

Here is a simple example of getting the list of devices on the subscriber using `SyncClient`:

```python
from machineq import SyncClient

client_id = "your-client-id
client_secret = "your-client-secret"

client = SyncClient(client_id, client_secret)
devices = client.devices.get_all()
print(devices)
```

## Features

- [x] Synchronous Client
- [x] Asynchronous Client
- [x] Strong Typing
- [ ] Enhanced Tracing
- [ ] V2 API implementation
- [ ] Enhanced Logging
- [ ] Built-in helpful tools (multi-page `get_logs`, bulk async provision)
- [ ] CLI tool
