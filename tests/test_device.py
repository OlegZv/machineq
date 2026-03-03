# """Tests for Device API."""

# import pytest
# from sample_data.common import (
#     random_deveui,
#     random_hex,
#     random_name,
# )

# from machineq.client import SyncClient, AsyncClient
# from machineq.core.device.api import SyncDevices, AsyncDevices
# from machineq.core.device.models import (
#     ActivationType,
#     DeviceCreate,
#     DevicePatch,
#     DeviceUpdate,
# )
# from machineq.core.output_profile import OutputProfileCreate


# @pytest.fixture
# async def devices_api(client) -> SyncDevices | AsyncDevices:
#     """Get devices API resource from whichever client is requested."""
#     return client.devices


# @pytest.mark.asyncio
# class TestDevices:
#     """Device API tests."""

#     async def test_get_all(self, devices_api):
#         """Test listing all devices."""
#         await devices_api.get_all()

#     async def test_get_existing_device(self, devices_api):
#         """Test retrieving a specific device."""
#         devices = await devices_api.get_all()
#         if devices:
#             deveui = devices[0].deveui
#             result = await devices_api.get(deveui)
#             assert result.deveui == deveui

#     async def test_create_and_delete(self, devices_api, client, get_service_profile, get_device_profile):
#         """Test creating and deleting a device."""
#         deveui = random_deveui()
#         data = DeviceCreate(
#             name=random_name(),
#             deveui=deveui,
#             activation_type=ActivationType.OTAA,
#             service_profile=get_service_profile(),
#             device_profile=get_device_profile(),
#             application_eui=random_hex(16),
#             application_key=random_hex(32),
#         )

#         created_deveui = await devices_api.create(data)

#         try:
#             assert created_deveui == deveui
#             device = await devices_api.get(deveui)
#             assert device.deveui == deveui
#         finally:
#             await devices_api.delete(deveui)

#     async def test_get_health(self, devices_api, client, get_service_profile, get_device_profile):
#         """Test getting device health. Create a device and check it appears in the offline list."""
#         deveui = random_deveui()
#         data = DeviceCreate(
#             name=random_name(),
#             deveui=deveui,
#             activation_type=ActivationType.OTAA,
#             service_profile=get_service_profile(),
#             device_profile=get_device_profile(),
#             application_eui=random_hex(16),
#             application_key=random_hex(32),
#         )

#         created_deveui = await devices_api.create(data)
#         try:
#             assert created_deveui == deveui

#             result = await devices_api.get_health()
#             offline_deveuis = [d.deveui for d in result.offline]
#             assert deveui in offline_deveuis
#         finally:
#             await devices_api.delete(deveui)

#     async def test_get_health_count(self, devices_api):
#         """Test getting device health count."""
#         await devices_api.get_health_count()
#         # for now just checking the response is returned and parsed

#     async def test_devices_update_and_patch(self, devices_api, client, get_service_profile, get_device_profile):
#         """Test updating and patching a device by creating and then modifying it."""
#         deveui = random_deveui()
#         data = DeviceCreate(
#             name=random_name(),
#             deveui=deveui,
#             activation_type=ActivationType.OTAA,
#             service_profile=get_service_profile(),
#             device_profile=get_device_profile(),
#             application_eui=random_hex(16),
#             application_key=random_hex(32),
#         )

#         created_deveui = await devices_api.create(data)
#         output_profile = ""

#         try:
#             # create output profile for update ad lates deletion
#             output_profile = await client.output_profiles.create(OutputProfileCreate(name=random_name()))
#             device = await devices_api.get(created_deveui)
#             assert device.deveui == created_deveui
#             assert not device.private_data
#             update_data = DeviceUpdate(
#                 name=random_name(),
#                 service_profile=device.service_profile,
#                 device_profile=device.device_profile,
#                 decoder_type=device.decoder_type,
#                 output_profile=output_profile,
#                 private_data=True,
#             )

#             updated = await devices_api.update(created_deveui, update_data)
#             assert updated

#             fetched = await devices_api.get(created_deveui)
#             assert fetched.deveui == created_deveui
#             assert fetched.name == update_data.name
#             assert fetched.private_data
#             assert fetched.output_profile == output_profile

#             patch_data = DevicePatch(
#                 name=random_name(),
#                 remove_output_profile=True,
#             )
#             patched = await devices_api.patch(created_deveui, patch_data)
#             assert patched
#             fetched = await devices_api.get(created_deveui)
#             assert fetched.deveui == created_deveui
#             assert fetched.name == patch_data.name
#             assert fetched.output_profile == ""

#         finally:
#             await devices_api.delete(created_deveui)
#             if output_profile:
#                 await client.output_profiles.delete(output_profile)
