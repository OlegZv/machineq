"""Tests for Output Profile API."""

import pytest
from async_test_client import AsyncTestClient
from conftest import ProfileGetter
from sample_data.common import random_deveui, random_name, random_password

from machineq.core.device.models import ActivationType, DeviceCreate
from machineq.core.output_profile import (
    OutputProfileAWSParams,
    OutputProfileDevicesUpdateResponse,
    OutputProfileMQTTParams,
    OutputProfileRestParams,
)
from machineq.core.output_profile.api import AsyncOutputProfiles
from machineq.core.output_profile.models import (
    OutputProfileCreate,
    OutputProfileDevicesUpdate,
    OutputProfilePatch,
    OutputProfileUpdate,
)


@pytest.fixture
def output_profiles_api(client: AsyncTestClient) -> AsyncOutputProfiles:
    """Get output profiles API resource from whichever client was requested."""
    return client.output_profiles


@pytest.mark.asyncio
class TestOutputProfiles:
    """Output Profile API tests."""

    async def test_get_all(self, output_profiles_api: AsyncOutputProfiles):
        """Test listing all output profiles."""
        await output_profiles_api.get_all()

    async def test_create_and_delete(self, output_profiles_api: AsyncOutputProfiles):
        """Test creating and deleting an output profile."""
        create_name = random_name()
        data = OutputProfileCreate(name=create_name)
        profile_id = await output_profiles_api.create(data)

        try:
            profile = await output_profiles_api.get(profile_id)
            assert profile.id == profile_id
            assert profile.name == create_name
            # all of the connection parameters should be empty lists
            assert profile.mqtt_params == []
            assert profile.rest_params == []
            assert profile.azure_params == []
            assert profile.aws_params == []
        finally:
            await output_profiles_api.delete(profile_id)

    async def test_output_profiles_update_and_patch(self, output_profiles_api: AsyncOutputProfiles):
        """Test updating and patching an output profile."""
        create_name = random_name()
        mqtt = OutputProfileMQTTParams(
            host="mqtt.example.com:8883", topic="test-topic", username="user", password=random_password()
        )
        data = OutputProfileCreate(name=create_name, mqtt_params=[mqtt])
        profile_id = await output_profiles_api.create(data)

        try:
            profile = await output_profiles_api.get(profile_id)
            assert profile.id == profile_id
            assert profile.name == create_name
            # the destination ID would be assigned by the API
            assert len(profile.mqtt_params) == 1
            assert profile.mqtt_params[0].host == mqtt.host
            assert profile.mqtt_params[0].topic == mqtt.topic
            assert profile.mqtt_params[0].username == mqtt.username
            assert profile.mqtt_params[0].password == mqtt.password
            assert profile.rest_params == []
            assert profile.azure_params == []
            assert profile.aws_params == []

            update_rest_params = OutputProfileRestParams(
                url="https://example.com/api/data",
            )
            update_name = random_name()
            update_data = OutputProfileUpdate(
                name=update_name,
                # remove MQTT params
                mqtt_params=[],
                rest_params=[update_rest_params],
                azure_params=[],
                aws_params=[],
            )

            updated = await output_profiles_api.update(profile_id, update_data)
            assert updated

            # verify the update
            fetched = await output_profiles_api.get(profile_id)
            assert fetched.id == profile_id
            assert fetched.name == update_name
            assert fetched.mqtt_params == []
            assert len(fetched.rest_params) == 1
            assert fetched.rest_params[0].url == update_rest_params.url
            assert fetched.azure_params == []
            assert fetched.aws_params == []

            patch_name = random_name()
            patch_aws = OutputProfileAWSParams(
                endpoint="someinvalidname.iot.us-east-1.amazonaws.com",
                x509_certificate="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
                private_key="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----",
            )
            patch_data = OutputProfilePatch(
                name=patch_name,
                # just add the aws params
                aws_params=[patch_aws],
            )
            patched = await output_profiles_api.patch(profile_id, patch_data)

            assert patched

            fetched = await output_profiles_api.get(profile_id)
            assert fetched.id == profile_id
            assert fetched.name == patch_name
            assert fetched.mqtt_params == []
            assert len(fetched.rest_params) == 1
            assert fetched.rest_params[0].url == update_rest_params.url
            assert fetched.azure_params == []
            assert len(fetched.aws_params) == 1
            assert fetched.aws_params[0].endpoint == patch_aws.endpoint
            assert fetched.aws_params[0].x509_certificate == patch_aws.x509_certificate
            assert fetched.aws_params[0].private_key == patch_aws.private_key

        finally:
            await output_profiles_api.delete(profile_id)

    async def test_output_profiles_update_devices_put(
        self,
        output_profiles_api: AsyncOutputProfiles,
        client: AsyncTestClient,
        get_service_profile: ProfileGetter,
        get_device_profile: ProfileGetter,
    ):
        """Test update_devices (PUT) for output profiles to associate devices."""
        data = OutputProfileCreate(name=random_name())
        profile_id = await output_profiles_api.create(data)
        # by default it's created with no associated devices
        profile = await output_profiles_api.get(profile_id)
        assert profile.id == profile_id
        assert profile.mqtt_params == []
        assert profile.rest_params == []
        assert profile.azure_params == []
        assert profile.aws_params == []

        test_device = ""
        test_device_2 = ""
        device_api = output_profiles_api.client.devices

        try:
            # create a device to associate

            deveui = random_deveui()
            deveui2 = random_deveui()
            new_device = DeviceCreate(
                name=random_name(),
                deveui=deveui,
                activation_type=ActivationType.OTAA,
                service_profile=get_service_profile(),
                device_profile=get_device_profile(),
                application_eui=deveui,
                application_key=deveui * 2,
            )
            test_device = await device_api.create(new_device)
            new_device.deveui = deveui2
            test_device_2 = await device_api.create(new_device)

            # first try patch by adding two devices one by one
            patch_data = OutputProfileDevicesUpdate(
                devices=[test_device],
            )
            patched = await output_profiles_api.add_devices(profile_id, patch_data)

            def assert_response_success(
                response: OutputProfileDevicesUpdateResponse, expected_deveuis: list[str]
            ) -> None:
                assert len(response.responses) == len(expected_deveuis)
                for resp, expected_deveui in zip(response.responses, expected_deveuis, strict=True):
                    assert resp.deveui == expected_deveui
                    assert resp.error == ""
                    assert resp.response

            assert_response_success(patched, [test_device])

            # make sure the device now has the output profile associated
            fetched_device = await device_api.get(test_device)
            assert fetched_device.output_profile == profile_id

            # add the second device
            patch_data = OutputProfileDevicesUpdate(
                devices=[test_device_2],
            )
            patched = await output_profiles_api.add_devices(profile_id, patch_data)
            assert_response_success(patched, [test_device_2])
            fetched_device_2 = await device_api.get(test_device_2)
            assert fetched_device_2.output_profile == profile_id
            # the first device should still be associated
            fetched_device = await device_api.get(test_device)
            assert fetched_device.output_profile == profile_id

            # Update will replace the existing associated devices with the new list
            update = OutputProfileDevicesUpdate(devices=[test_device])
            resp = await output_profiles_api.update_devices(profile_id, update)
            assert_response_success(resp, [test_device])
            fetched_device = await device_api.get(test_device)
            assert fetched_device.output_profile == profile_id
            # the second device should no longer be associated
            fetched_device_2 = await device_api.get(test_device_2)
            assert fetched_device_2.output_profile == ""
        finally:
            await output_profiles_api.delete(profile_id)
            if test_device:
                await device_api.delete(test_device)
            if test_device_2:
                await device_api.delete(test_device_2)
