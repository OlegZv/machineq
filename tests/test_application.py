"""Tests for Application API."""

import asyncio

import pytest
from sample_data.common import random_name

from machineq import MqAuth
from machineq.auth import AuthenticationException
from machineq.client.sync import SyncClient
from machineq.core.application import ApplicationPatch, ApplicationUpdate
from machineq.core.application.api import AsyncApplications, SyncApplications
from machineq.core.application.models import ApplicationCreate


@pytest.fixture
def applications_api(client) -> SyncApplications | AsyncApplications:
    """Get applications API resource."""
    return client.applications


@pytest.mark.asyncio
class TestApplications:
    """Application API tests."""

    async def test_get_all(self, applications_api):
        """Test listing all applications."""
        result = await applications_api.get_all()
        # these tests run through an application so at least one should be there
        assert len(result) > 0

    async def test_create_and_delete(self, applications_api):
        """Test creating and deleting an application."""
        # first get any role to assocaite with the application
        role_id = await self.get_a_role(applications_api)
        data = ApplicationCreate(name=random_name(), roles=[role_id])
        application = await applications_api.create(data)
        # assert that we just created an application with the expected data
        assert application.id

        try:
            assert application.name == data.name
            assert application.UUID
            assert application.client_secret

            # validate get
            app = await applications_api.get(application.id)
            assert app.id == application.id
            assert app.name == data.name
            assert set(app.roles) == {role_id}
            assert app.subscriber_id
            assert app.UUID == application.UUID

            # validate get all includes this application
            all_apps = await applications_api.get_all()
            assert any(a.id == application.id for a in all_apps)

        finally:
            await applications_api.delete(application.id)

    async def test_modify(self, applications_api: AsyncApplications):
        """Test modifying an application."""
        # create an application to modify
        data = ApplicationCreate(name=random_name(), roles=[])
        application = await applications_api.create(data)
        assert application.id

        try:
            # update the application's name and add a role
            roles = await applications_api.client.roles.get_all()
            assert len(roles) > 0
            # for now verifying the role is accepted. in the future would be nice to create more roles
            # and verify the correct one is added
            role_id = roles[0].id
            update_data = ApplicationUpdate(name=random_name(), roles=[role_id])
            updated = await applications_api.update(application.id, update_data)
            assert updated
            updated_app = await applications_api.get(application.id)
            assert updated_app.id == application.id
            assert updated_app.name == update_data.name
            assert set(updated_app.roles) == {role_id}
            assert updated_app.UUID == application.UUID

            # only update the name using a patch
            patch_data = ApplicationPatch(name=random_name())
            patched = await applications_api.patch(application.id, patch_data)
            assert patched
            patched_app = await applications_api.get(application.id)
            assert patched_app.id == application.id
            assert patched_app.name == patch_data.name
            assert set(patched_app.roles) == {role_id}
            assert patched_app.UUID == application.UUID

        finally:
            await applications_api.delete(application.id)

    async def test_refresh(self, applications_api):
        """Test refreshing an application's token."""
        # create an application to refresh
        role = await self.get_a_role(applications_api)
        data = ApplicationCreate(name=random_name(), roles=[role])
        application = await applications_api.create(data)
        assert application.id
        created_application = await applications_api.get(application.id)
        assert created_application.UUID == application.UUID
        try:
            # give some time for the application to be fully created before trying to use it
            await asyncio.sleep(2)
            # ensure we can get a token with this application
            new_auth = MqAuth(application.UUID, application.client_secret)
            assert new_auth.token != ""

            # ensure it actually works by calling a protected API
            client1 = SyncClient(application.UUID, application.client_secret)
            response = client1.account.get()
            # subscriber ID has to match since we operate on a single subscriber
            assert response.subscriber_info.id == created_application.subscriber_id
            # test refresh
            new_secret = await applications_api.refresh_token(application.id)
            assert new_secret != application.client_secret
            await asyncio.sleep(3)
            # ensure the new secret works
            new_client = SyncClient(application.UUID, new_secret)
            response = new_client.account.get()
            assert response.subscriber_info.id == created_application.subscriber_id

            # the old client_secret should be invalid now
            with pytest.raises(AuthenticationException):
                client1.auth.refresh()

        finally:
            await applications_api.delete(application.id)

    async def get_a_role(self, applications_api) -> str:
        """Helper to get a role ID for testing."""
        roles = await applications_api.client.roles.get_all()
        assert len(roles) > 0
        return roles[0].id
