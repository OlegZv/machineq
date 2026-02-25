"""Tests for Application API."""

from time import sleep

import pytest
from sample_data.common import random_name

from machineq import MqAuth
from machineq.auth import AuthenticationException
from machineq.client.sync import SyncClient
from machineq.core.application import ApplicationPatch, ApplicationUpdate
from machineq.core.application.api import SyncApplications
from machineq.core.application.models import ApplicationCreate


@pytest.fixture
def applications_api(sync_client: SyncClient) -> SyncApplications:
    """Get applications API resource."""
    return sync_client.applications


class TestApplications:
    """Application API tests."""

    def test_get_all(self, applications_api: SyncApplications):
        """Test listing all applications."""
        result = applications_api.get_all()
        # these tests run through an application so at least one should be there
        assert len(result) > 0

    def test_create_and_delete(self, applications_api: SyncApplications):
        """Test creating and deleting an application."""
        # first get any role to assocaite with the application
        role_id = self.get_a_role(applications_api)
        data = ApplicationCreate(name=random_name(), roles=[self.get_a_role(applications_api)])
        application = applications_api.create(data)
        # assert that we just created an application with the expected data
        assert application.id

        try:
            assert application.name == data.name
            assert application.UUID
            assert application.client_secret

            # validate get
            app = applications_api.get(application.id)
            assert app.id == application.id
            assert app.name == data.name
            assert set(app.roles) == {role_id}
            assert app.subscriber_id
            assert app.UUID == application.UUID

            # validate get all includes this application
            all_apps = applications_api.get_all()
            assert any(a.id == application.id for a in all_apps)

        finally:
            applications_api.delete(application.id)

    def test_modify(self, applications_api: SyncApplications):
        """Test modifying an application."""
        # create an application to modify
        data = ApplicationCreate(name=random_name(), roles=[])
        application = applications_api.create(data)
        assert application.id

        try:
            # update the application's name and add a role
            roles = applications_api.client.roles.get_all()
            assert len(roles) > 0
            # for now verifying the role is accepted. in the future would be nice to create more roles
            # and verify the correct one is added
            role_id = roles[0].id
            update_data = ApplicationUpdate(name=random_name(), roles=[role_id])
            updated = applications_api.update(application.id, update_data)
            assert updated
            updated_app = applications_api.get(application.id)
            assert updated_app.id == application.id
            assert updated_app.name == update_data.name
            assert set(updated_app.roles) == {role_id}
            assert updated_app.UUID == application.UUID

            # only update the name using a patch
            patch_data = ApplicationPatch(name=random_name())
            patched = applications_api.patch(application.id, patch_data)
            assert patched
            patched_app = applications_api.get(application.id)
            assert patched_app.id == application.id
            assert patched_app.name == patch_data.name
            assert set(patched_app.roles) == {role_id}
            assert patched_app.UUID == application.UUID

        finally:
            applications_api.delete(application.id)

    def test_refresh(self, applications_api: SyncApplications):
        """Test refreshing an application's token."""
        # create an application to refresh
        data = ApplicationCreate(name=random_name(), roles=[self.get_a_role(applications_api)])
        application = applications_api.create(data)
        assert application.id
        created_application = applications_api.get(application.id)
        assert created_application.UUID == application.UUID
        try:
            # give some time for the application to be fully created before trying to use it
            sleep(1)
            # ensure we can get a token with this application
            new_auth = MqAuth(application.UUID, application.client_secret)
            assert new_auth.token != ""

            # ensure it actually works by calling a protected API
            client1 = SyncClient(application.UUID, application.client_secret)
            response = client1.account.get()
            # subscriber ID has to match since we operate on a single subscriber
            assert response.subscriber_info.id == created_application.subscriber_id
            # test refresh
            new_secret = applications_api.refresh_token(application.id)
            assert new_secret != application.client_secret

            # ensure the new secret works
            new_client = SyncClient(application.UUID, new_secret)
            response = new_client.account.get()
            assert response.subscriber_info.id == created_application.subscriber_id

            # the old client_secret should be invalid now
            with pytest.raises(AuthenticationException):
                client1.auth.refresh()

        finally:
            applications_api.delete(application.id)

    def get_a_role(self, applications_api: SyncApplications) -> str:
        """Helper to get a role ID for testing."""
        roles = applications_api.client.roles.get_all()
        assert len(roles) > 0
        return roles[0].id
