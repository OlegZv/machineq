"""Asynchronous client for MachineQ API."""

from __future__ import annotations

import httpx

from machineq.auth import MqApiEnvironment, MqAuth
from machineq.core.account.api import AsyncAccount
from machineq.core.application.api import AsyncApplications
from machineq.core.decoder_type.api import AsyncDecoderTypes
from machineq.core.device.api import AsyncDevices
from machineq.core.device_group.api import AsyncDeviceGroups
from machineq.core.device_profile.api import AsyncDeviceProfiles
from machineq.core.gateway.api import AsyncGateways
from machineq.core.gateway_group.api import AsyncGatewayGroups
from machineq.core.gateway_profile.api import AsyncGatewayProfiles
from machineq.core.logs.api import AsyncLogs
from machineq.core.multicast_group.api import AsyncMulticastGroups
from machineq.core.output_profile.api import AsyncOutputProfiles
from machineq.core.rf_region.api import AsyncRFRegions
from machineq.core.role.api import AsyncRoles
from machineq.core.service_profile.api import AsyncServiceProfiles
from machineq.core.users.api import AsyncUsers
from machineq.core.version.api import AsyncVersion
from machineq.utils import __version__


class AsyncClient:
    """Asynchronous client for MachineQ API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        version: str = "v1",
        extra_prefix: str = "",
        env: MqApiEnvironment = MqApiEnvironment.PROD,
    ):
        """Initialize async client.

        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret
            base_url: Base URL for API (default: production v1)
            env: API environment (default: production)
        """
        # Create auth with a sync client (token refresh is always synchronous)
        self.auth = MqAuth(
            client_id=client_id,
            client_secret=client_secret,
            env=env,
        )
        self.api_version = version
        self.extra_prefix = extra_prefix
        self.http_client = httpx.AsyncClient(headers={"User-Agent": f"machineq-py/{__version__}"})

        # Initialize all resource attributes
        self.account = AsyncAccount(self)
        self.applications = AsyncApplications(self)
        self.decoder_types = AsyncDecoderTypes(self)
        self.devices = AsyncDevices(self)
        self.device_groups = AsyncDeviceGroups(self)
        self.device_profiles = AsyncDeviceProfiles(self)
        self.gateways = AsyncGateways(self)
        self.gateway_groups = AsyncGatewayGroups(self)
        self.gateway_profiles = AsyncGatewayProfiles(self)
        self.logs = AsyncLogs(self)
        self.multicast_groups = AsyncMulticastGroups(self)
        self.output_profiles = AsyncOutputProfiles(self)
        self.rf_regions = AsyncRFRegions(self)
        self.roles = AsyncRoles(self)
        self.service_profiles = AsyncServiceProfiles(self)
        self.users = AsyncUsers(self)
        self.version = AsyncVersion(self)

    async def aclose(self) -> None:
        """Close the underlying HTTP client session."""
        await self.http_client.aclose()

    async def __aenter__(self) -> AsyncClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.http_client.aclose()
