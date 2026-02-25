"""Common utility functions for generating sample data."""

# ruff: noqa: S311 (because these random generators are only used for testing purposes)
import random
import string
from datetime import UTC, datetime, timedelta


def random_part(length: int = 8) -> str:
    """Generate a random alphanumeric string."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_id() -> str:
    """Generate a random ID."""
    return random_part(16)


def random_email() -> str:
    """Generate a random email."""
    return f"testuser_{random_part(8)}@example.com"


def random_name() -> str:
    """Generate a random name."""
    return f"TestObject_{random_part(8)}"


def random_password() -> str:
    """Generate a random password."""
    return random_part(16) + "*"


def random_deveui() -> str:
    """Generate a random DevEUI (16 hex characters)."""
    return "".join(random.choices(string.hexdigits[:16], k=16)).upper()


def random_gateway_id() -> str:
    """Generate a random Gateway ID (16 hex characters)."""
    return "".join(random.choices(string.hexdigits[:16], k=16)).upper()


def random_mac_address() -> str:
    """Generate a random MAC address."""
    return ":".join("".join(random.choices(string.hexdigits[:16], k=2)).upper() for _ in range(6))


def random_hex(length: int = 32) -> str:
    """Generate a random hex string."""
    return "".join(random.choices(string.hexdigits[:16], k=length)).upper()


def iso_timestamp(offset_days: int = 0) -> str:
    """Generate an ISO 8601 timestamp."""
    dt = datetime.now(UTC) + timedelta(days=offset_days)
    return dt.isoformat() + "Z"


# Standard IDs for testing (can reuse across tests)
TEST_DEVICE_EUIS = [random_deveui() for _ in range(5)]
TEST_GATEWAY_IDS = [random_gateway_id() for _ in range(5)]
