"""Tests for Output Profile API."""

import pytest
from sample_data.common import random_name

from machineq.client.sync import SyncClient
from machineq.core.output_profile.api import SyncOutputProfiles
from machineq.core.output_profile.models import OutputProfileCreate


@pytest.fixture
def output_profiles_api(sync_client: SyncClient) -> SyncOutputProfiles:
    """Get output profiles API resource."""
    return sync_client.output_profiles


class TestOutputProfiles:
    """Output Profile API tests."""

    def test_get_all(self, output_profiles_api: SyncOutputProfiles):
        """Test listing all output profiles."""
        output_profiles_api.get_all()

    def test_create_and_delete(self, output_profiles_api: SyncOutputProfiles):
        """Test creating and deleting an output profile."""
        data = OutputProfileCreate(name=random_name())
        profile_id = output_profiles_api.create(data)

        try:
            profile = output_profiles_api.get(profile_id)
            assert profile.id == profile_id
        finally:
            output_profiles_api.delete(profile_id)
