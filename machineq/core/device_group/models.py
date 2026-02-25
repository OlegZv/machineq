from machineq.core.shared.models import BaseModelWithConfig

from ..device.models import DeviceInstance


class DeviceGroupCreate(BaseModelWithConfig):
    name: str
    device_list: list[str] | None


class DeviceGroupCreateResponse(BaseModelWithConfig):
    id: str


class DeviceGroupError(BaseModelWithConfig):
    response: bool


class DeviceGroupInstance(BaseModelWithConfig):
    id: str
    name: str
    device_list: list[str]
    devices: list[DeviceInstance]


class DeviceGroupPatch(BaseModelWithConfig):
    id: str
    name: str | None
    device_list: list[str] | None


class DeviceGroupResponse(BaseModelWithConfig):
    device_groups: list[DeviceGroupInstance]


class DeviceGroupUpdate(BaseModelWithConfig):
    id: str
    name: str
    device_list: list[str] | None


class GetDeviceGroupRecentResponse(BaseModelWithConfig):
    device_list: list[str]
