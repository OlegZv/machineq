"""Tests for Users API."""

import logging

import pytest
from sample_data.common import random_email, random_name, random_password

from machineq.core.users.api import AsyncUsers, SyncUsers
from machineq.core.users.models import UserCreate, UserPatch, UserUpdate


@pytest.fixture
def users_api(client) -> SyncUsers | AsyncUsers:
    """Get users API resource from whichever client was requested."""
    return client.users


@pytest.mark.asyncio
class TestUsers:
    """Users API tests."""

    async def test_get_all(self, users_api):
        """Test listing all users."""
        await users_api.get_all()

    async def test_create_and_delete(self, users_api):
        """Test creating and deleting a user."""
        data = UserCreate(
            email=random_email(),
            username=random_name(),
            first_name="Test",
            last_name="User",
            password=random_password(),
            phone_number="123-456-7890",
        )

        user_id = await users_api.create(data)

        try:
            user = await users_api.get(user_id)
            assert user.id == user_id
        finally:
            await users_api.delete(user_id)

    async def test_users_update_full(self, users_api):
        """Test updating a user (full replacement) and verifying the result."""
        # create initial user
        data = UserCreate(
            email=random_email(),
            username=random_name(),
            first_name="Initial",
            last_name="User",
            password=random_password(),
            phone_number="111-222-3333",
        )

        user_id = await users_api.create(data)

        try:
            # perform a full update (replace)
            roles = await self.roles(users_api)
            assert len(roles) > 0
            any_role_id = roles[0]
            update_email = random_email()
            update_data = UserUpdate(
                email=update_email,
                first_name="Updated",
                last_name="User2",
                phone_number="999-888-7777",
                password=random_password(),
                roles=[],
            )

            updated = await users_api.update(user_id, update_data)
            assert updated

            # verify via get
            fetched = await users_api.get(user_id)
            assert fetched.id == user_id
            assert fetched.first_name == "Updated"
            assert fetched.last_name == "User2"
            assert fetched.phone_number == "999-888-7777"
            assert fetched.roles == [""]
            assert fetched.email == update_email

            # patch different fields and ensure the update
            patch_email = random_email()
            patch_fields = {
                "roles": [any_role_id],
                "first_name": "Patched",
                "last_name": "User3",
                "phone_number": "555-444-3333",
                "email": patch_email,
                # not checking assword since can't really verify
            }
            for field, value in patch_fields.items():
                logging.info(f"Patching field {field} to value {value}")
                patch_data = UserPatch()
                setattr(patch_data, field, value)
                patched = await users_api.patch(user_id, patch_data)
                assert patched

                fetched = await users_api.get(user_id)
                assert getattr(fetched, field) == value

        finally:
            await users_api.delete(user_id)

    async def roles(self, user_api) -> list[str]:
        """Helper to get an existing role for update payload."""
        roles = await user_api.client.roles.get_all()
        if not roles:
            pytest.skip("No roles available to assign to user.")
        return [role.id for role in roles]
