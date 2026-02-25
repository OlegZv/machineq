from datetime import datetime
from enum import Enum
from typing import Any

from machineq.core.shared.models import BaseModelWithConfig

from ..decoder_type.models import PayloadDecoderType
from ..output_profile.models import OutputProfileInstance


class ActivationType(str, Enum):
    OTAA = "OTAA"
    ABP = "ABP"


class DeviceStatistics(BaseModelWithConfig):
    health_state: str
    spreading_factor: int
    average_rssi: float
    average_esp: float
    average_snr: float
    packet_error_rate: float
    battery_level: int
    average_weekly_packets: int


class DeviceInstance(BaseModelWithConfig):
    name: str
    deveui: str
    activation_type: str
    service_profile: str
    device_profile: str
    decoder_type: str
    output_profile: str
    private_data: bool
    created_at: datetime
    updated_at: datetime
    updated_by: str
    last_uplink: datetime | None
    statistics: DeviceStatistics
    payload_decoder: PayloadDecoderType


class DeviceCreate(BaseModelWithConfig):
    name: str
    deveui: str
    dev_addr: str | None = None
    network_skey: str | None = None
    activation_type: ActivationType
    application_eui: str | None = None
    application_key: str | None = None
    application_s_key: str | None = None
    service_profile: str
    device_profile: str
    decoder_type: str | None = None
    output_profile: str | None = None
    private_data: bool = False
    network_s_key: str | None = None


class DeviceCreateResponse(BaseModelWithConfig):
    id: str


class DeviceError(BaseModelWithConfig):
    response: bool


class DeviceFilter(BaseModelWithConfig):
    deveui: str


class DeviceMessage(BaseModelWithConfig):
    deveui: str
    payload: str | None
    target_port: str | None
    confirm: bool | None
    flush_queue: bool | None
    application_payload: dict[str, Any] | None


class DevicePatch(BaseModelWithConfig):
    name: str
    deveui: str
    service_profile: str | None
    device_profile: str | None
    decoder_type: str | None
    output_profile: str | None
    private_data: bool | None
    remove_output_profile: bool | None


class DevicePayload(BaseModelWithConfig):
    time: str
    data: dict[str, Any]
    application_data: dict[str, Any]


class DevicePayloadResponse(BaseModelWithConfig):
    payloads: list[DevicePayload]


class DeviceResponse(BaseModelWithConfig):
    devices: list[DeviceInstance]


class DeviceUpdate(BaseModelWithConfig):
    name: str
    deveui: str
    service_profile: str
    device_profile: str
    decoder_type: str | None
    output_profile: str | None
    private_data: bool | None


class CreateDevicesResponse(BaseModelWithConfig):
    response: bool
    deveui: str
    error: str
    id: str


class DeleteDevicesResponse(BaseModelWithConfig):
    response: bool
    deveui: str
    error: str


class DeviceConfigInfo(BaseModelWithConfig):
    name: str
    deveui: str
    dev_addr: str
    private_data: bool
    decoder_type: str
    output_profile: OutputProfileInstance
    activation_type: str
    subscriber_id: str
    application_s_key: str
    network_server_type: str


class DevicesHealthCountResponse(BaseModelWithConfig):
    good: int
    fair: int
    poor: int
    offline: int


class DevicesHealthResponse(BaseModelWithConfig):
    good: list[DeviceInstance]
    fair: list[DeviceInstance]
    poor: list[DeviceInstance]
    offline: list[DeviceInstance]
