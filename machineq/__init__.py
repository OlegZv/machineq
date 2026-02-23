"""MachineQ Python API client."""

from machineq.auth import MqApiEnvironment, MqAuth
from machineq.client import (
    APIError,
    AsyncClient,
    MachineQError,
    NotFound,
    PermissionDenied,
    SyncClient,
    Unauthorized,
    ValidationError,
)

__version__ = "0.0.1"

__all__ = [
    "APIError",
    "AsyncClient",
    # Exceptions
    "MachineQError",
    "MqApiEnvironment",
    # Auth
    "MqAuth",
    "NotFound",
    "PermissionDenied",
    # Clients
    "SyncClient",
    "Unauthorized",
    "ValidationError",
    "create_client",
]
