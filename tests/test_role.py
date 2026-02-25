"""Tests for Role API."""

import pytest
from sample_data.common import random_name

from machineq.client.sync import SyncClient
from machineq.core.role.api import SyncRoles
from machineq.core.role.models import RoleCreate


@pytest.fixture
def roles_api(sync_client: SyncClient) -> SyncRoles:
    """Get roles API resource."""
    return sync_client.roles


class TestRoles:
    """Role API tests."""

    def test_get_all(self, roles_api: SyncRoles):
        """Test listing all roles."""
        result = roles_api.get_all()
        assert len(result) > 0

    def test_create_and_delete(self, roles_api: SyncRoles):
        """Test creating and deleting a role."""
        data = RoleCreate(name=random_name())
        role_id = roles_api.create(data)

        try:
            role = roles_api.get(role_id)
            assert role.id == role_id
        finally:
            roles_api.delete(role_id)
