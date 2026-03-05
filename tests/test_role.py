"""Tests for Role API."""

import pytest
from async_test_client import AsyncTestClient
from sample_data.common import random_email, random_name, random_password

from machineq.core.account import PermissionObject
from machineq.core.application import ApplicationCreate
from machineq.core.role.api import AsyncRoles
from machineq.core.role.models import RoleCreate, RolePatch, RoleUpdate
from machineq.core.users import UserCreate


@pytest.fixture
def roles_api(client: AsyncTestClient) -> AsyncRoles:
    """Get roles API resource from whichever client was requested."""
    return client.roles


def verify_permissions(
    permissions: PermissionObject | None,
    read: bool = False,
    create: bool = False,
    update: bool = False,
    delete: bool = False,
):
    """Helper function to verify permissions."""
    if permissions is None and not any([read, create, update, delete]):
        return
    assert permissions is not None
    assert permissions.read == read
    assert permissions.create == create
    assert permissions.update == update
    assert permissions.delete == delete


@pytest.mark.asyncio
class TestRoles:
    """Role API tests."""

    async def test_get_all(self, roles_api: AsyncRoles):
        """Test listing all roles."""
        result = await roles_api.get_all()
        assert len(result) > 0

    async def test_create_and_delete(self, roles_api: AsyncRoles):
        """Test creating and deleting a role."""
        data = RoleCreate(name=random_name())
        role_id = await roles_api.create(data)

        try:
            role = await roles_api.get(role_id)
            assert role.id == role_id
            # verify all permissions are false by default
            for perm in [role.device, role.user, role.gateway]:
                verify_permissions(perm)
        finally:
            await roles_api.delete(role_id)

    async def test_role_update_and_patch(self, roles_api: AsyncRoles):
        """Test updating and patching a role."""
        # all permissions are off
        data = RoleCreate(name=random_name())
        role_id = await roles_api.create(data)

        try:
            role = await roles_api.get(role_id)
            update_name = random_name()
            update_data = RoleUpdate(
                name=update_name,
                device=PermissionObject(read=True, create=False, update=False, delete=False),
                user=None,
                gateway=None,
                users=role.users,
                applications=role.applications,
            )

            updated = await roles_api.update(role_id, update_data)
            assert updated

            # verify the update via get
            fetched = await roles_api.get(role_id)
            assert fetched.id == role_id
            assert fetched.name == update_name
            verify_permissions(fetched.device, read=True, create=False, update=False, delete=False)
            verify_permissions(fetched.user)
            verify_permissions(fetched.gateway)
            # patch each field separately
            patch_name = random_name()
            field_patchs = {
                "name": patch_name,
                "device": PermissionObject(read=True, create=False, update=True, delete=False),
                "user": PermissionObject(read=False, create=True, update=False, delete=True),
                "gateway": PermissionObject(read=True, create=True, update=True, delete=True),
            }
            for field, value in field_patchs.items():
                patch_data = RolePatch()
                setattr(patch_data, field, value)
                patched = await roles_api.patch(role_id, patch_data)
                assert patched

                fetched = await roles_api.get(role_id)
                assert fetched.id == role_id
                result_field = getattr(fetched, field)
                if isinstance(value, PermissionObject):
                    verify_permissions(result_field, **value.model_dump(by_alias=False))
                else:
                    assert result_field == value

        finally:
            await roles_api.delete(role_id)

    async def test_create_update_patch_user_app(self, client: AsyncTestClient):
        """This test checks that we can create a role, assign it to a user (at create),
        reassign to the app only (update), then assign to both (patch)"""
        role = None
        user_id = ""
        app_id = ""

        try:
            # create a user
            users_api = client.users
            user_data = UserCreate(
                email=random_email(),
                username=random_name(),
                first_name="Test",
                last_name="User",
                password=random_password(),
                phone_number="123-456-7890",
            )
            user_id = await users_api.create(user_data)
            # create an app
            app_api = client.applications
            app_data = ApplicationCreate(name=random_name(), roles=[])
            app_id = (await app_api.create(app_data)).id

            # create role with user assignment
            data = RoleCreate(name=random_name(), user=PermissionObject(read=True), users=[user_id])
            role_id = await client.roles.create(data)

            role = await client.roles.get(role_id)
            assert role.id == role_id
            verify_permissions(role.user, read=True)
            verify_permissions(role.device)
            verify_permissions(role.gateway)
            assert role.users == [user_id]

            # check that the user has the role permissions
            user = await users_api.get(user_id)
            assert user.id == user_id
            assert user.roles == [role_id]

            # update to app only
            update_data = RoleUpdate(
                name=role.name,
                user=None,
                device=role.device,
                gateway=role.gateway,
                # remove user, add app
                users=[""],
                applications=[app_id],
            )
            updated = await client.roles.update(role_id, update_data)
            assert updated

            role = await client.roles.get(role_id)
            assert role.id == role_id
            assert role.user is None
            assert role.users == [""]
            assert role.applications == [app_id]
            # the app should have the role
            app = await app_api.get(app_id)
            assert app.id == app_id
            assert app.roles == [role_id]

            # patch to both user and app
            patch_data = RolePatch(user=PermissionObject(read=True), users=[user_id], applications=[app_id])
            patched = await client.roles.patch(role_id, patch_data)
            assert patched

            role = await client.roles.get(role_id)
            assert role.id == role_id
            assert role.user is not None
            assert role.users == [user_id]
            assert role.applications == [app_id]
        finally:
            if role is not None:
                await client.roles.delete(role.id)
            if user_id:
                await client.users.delete(user_id)
            if app_id:
                await client.applications.delete(app_id)
