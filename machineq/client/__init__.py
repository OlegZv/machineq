"""MachineQ API client factory and public exports."""

from __future__ import annotations

from .async_ import AsyncClient
from .exceptions import (
    APIError,
    InternalServerError,
    InvalidArgument,
    MachineQError,
    NotFound,
    PermissionDenied,
    RateLimited,
    ServiceUnavailable,
    Unauthenticated,
    Unauthorized,
    ValidationError,
)
from .sync import SyncClient

__all__ = [
    "APIError",
    "AsyncClient",
    "InternalServerError",
    "InvalidArgument",
    # Exceptions
    "MachineQError",
    "NotFound",
    "PermissionDenied",
    "RateLimited",
    "ServiceUnavailable",
    # Clients
    "SyncClient",
    "Unauthenticated",
    "Unauthorized",
    "ValidationError",
]
