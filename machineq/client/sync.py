"""Synchronous client for MachineQ API."""

from __future__ import annotations

import httpx

from machineq.auth import MqApiEnvironment, MqAuth
from machineq.core.account.api import SyncAccount
from machineq.core.application.api import SyncApplications
from machineq.core.decoder_type.api import SyncDecoderTypes
from machineq.core.device.api import SyncDevices
from machineq.core.device_group.api import SyncDeviceGroups
from machineq.core.device_profile.api import SyncDeviceProfiles
from machineq.core.gateway.api import SyncGateways
from machineq.core.gateway_group.api import SyncGatewayGroups
from machineq.core.gateway_profile.api import SyncGatewayProfiles
from machineq.core.logs.api import SyncLogs
from machineq.core.multicast_group.api import SyncMulticastGroups
from machineq.core.output_profile.api import SyncOutputProfiles
from machineq.core.rf_region.api import SyncRFRegions
from machineq.core.role.api import SyncRoles
from machineq.core.service_profile.api import SyncServiceProfiles
from machineq.core.users.api import SyncUsers
from machineq.core.version.api import SyncVersion


class SyncClient:
    """Synchronous client for MachineQ API."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = "https://api.machineq.net/v1",
        env: MqApiEnvironment = MqApiEnvironment.PROD,
    ):
        """Initialize sync client.

        Args:
            client_id: OAuth client ID
            client_secret: OAuth client secret
            base_url: Base URL for API (default: production v1)
            env: API environment (default: production)
        """
        # Create HTTP client for this sync client
        http_client = httpx.Client()
        # Create auth with the sync client
        self.auth = MqAuth(
            client_id=client_id,
            client_secret=client_secret,
            client=http_client,
            env=env,
        )
        self.base_url = base_url
        self.http_client = http_client

        # Initialize all resource attributes
        self.account = SyncAccount(self)
        self.applications = SyncApplications(self)
        self.decoder_types = SyncDecoderTypes(self)
        self.devices = SyncDevices(self)
        self.device_groups = SyncDeviceGroups(self)
        self.device_profiles = SyncDeviceProfiles(self)
        self.gateways = SyncGateways(self)
        self.gateway_groups = SyncGatewayGroups(self)
        self.gateway_profiles = SyncGatewayProfiles(self)
        self.logs = SyncLogs(self)
        self.multicast_groups = SyncMulticastGroups(self)
        self.output_profiles = SyncOutputProfiles(self)
        self.rf_regions = SyncRFRegions(self)
        self.roles = SyncRoles(self)
        self.service_profiles = SyncServiceProfiles(self)
        self.users = SyncUsers(self)
        self.version = SyncVersion(self)

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        self.http_client.close()

    def __enter__(self) -> SyncClient:
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
