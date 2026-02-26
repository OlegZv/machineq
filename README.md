# machineq

[![Release](https://img.shields.io/github/v/release/OlegZv/machineq)](https://img.shields.io/github/v/release/OlegZv/machineq)
[![Build status](https://img.shields.io/github/actions/workflow/status/OlegZv/machineq/main.yml?branch=main)](https://github.com/OlegZv/machineq/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/OlegZv/machineq/branch/main/graph/badge.svg)](https://codecov.io/gh/OlegZv/machineq)
[![Commit activity](https://img.shields.io/github/commit-activity/m/OlegZv/machineq)](https://img.shields.io/github/commit-activity/m/OlegZv/machineq)
[![License](https://img.shields.io/github/license/OlegZv/machineq)](https://img.shields.io/github/license/OlegZv/machineq)


## Example Usage

More docs to come, for now here's a simple example on how to use the package:
```python
from machineq.client import SyncClient

client_id = ""
client_secret = ""

client = SyncClient(client_id, client_secret)
devices = client.devices.get_all()
print(devices)
```
