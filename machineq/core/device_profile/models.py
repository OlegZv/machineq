from machineq.core.shared.models import BaseModelWithConfig


class DeviceProfileInstance(BaseModelWithConfig):
    id: str
    name: str


class DeviceProfileResponse(BaseModelWithConfig):
    device_profiles: list[DeviceProfileInstance]


class DeviceProfileDevicesResponse(BaseModelWithConfig):
    deveui: str
    response: bool
    error: str


class DeviceProfileDevicesUpdate(BaseModelWithConfig):
    id: str
    devices: list[str] | None


class DeviceProfileDevicesUpdateResponse(BaseModelWithConfig):
    responses: list[DeviceProfileDevicesResponse]
