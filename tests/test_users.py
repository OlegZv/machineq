"""Tests for Users API."""

import pytest
from sample_data.common import random_email, random_name, random_password

from machineq.client.sync import SyncClient
from machineq.core.users.api import SyncUsers
from machineq.core.users.models import UserCreate


@pytest.fixture
def users_api(sync_client: SyncClient) -> SyncUsers:
    """Get users API resource."""
    return sync_client.users


class TestUsers:
    """Users API tests."""

    def test_get_all(self, users_api: SyncUsers):
        """Test listing all users."""
        users_api.get_all()

    def test_create_and_delete(self, users_api: SyncUsers):
        """Test creating and deleting a user."""
        data = UserCreate(
            email=random_email(),
            username=random_name(),
            first_name="Test",
            last_name="User",
            password=random_password(),
            phone_number="123-456-7890",
        )

        user_id = users_api.create(data)

        try:
            user = users_api.get(user_id)
            assert user.id == user_id
        finally:
            users_api.delete(user_id)
