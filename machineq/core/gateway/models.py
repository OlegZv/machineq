import enum
from datetime import datetime

from pydantic import Field

from machineq.core.shared.models import BaseModelWithConfig


class Coordinates(BaseModelWithConfig):
    X: str
    Y: str
    Z: str = "1"


class LocationType(str, enum.Enum):
    INDOOR = "INDOOR"
    OUTDOOR = "OUTDOOR"


class GatewayEventField(str, enum.Enum):
    UNKNOWN = "UNKNOWN"
    BACKHAUL = "BACKHAUL"
    NS_CONNECT = "NS_CONNECT"
    ONLINE_STATUS = "ONLINE_STATUS"
    PACKET_FORWARDER = "PACKET_FORWARDER"
    REBOOT_TIME = "REBOOT_TIME"
    BACKHAUL_CONNECTED = "BACKHAUL_CONNECTED"
    BACKHAUL_DISCONNECTED = "BACKHAUL_DISCONNECTED"
    PACKET_FORWARDER_CONNECTED = "PACKET_FORWARDER_CONNECTED"
    PACKET_FORWARDER_DISCONNECTED = "PACKET_FORWARDER_DISCONNECTED"
    PUSH_RF_CONFIG = "PUSH_RF_CONFIG"


class GatewayGpsSyncStatus(str, enum.Enum):
    LOCKING_OR_NO_SIGNAL = "LOCKING_OR_NO_SIGNAL"
    LOCKED = "LOCKED"


class GatewayTimeSyncStatus(str, enum.Enum):
    LOCAL = "LOCAL"
    NTP = "NTP"
    GPS = "GPS"


class GatewayLocationType(str, enum.Enum):
    LOCATION_UNKNOWN = "LOCATION_UNKNOWN"
    LOCATION_ADMINISTRATIVELY = "LOCATION_ADMINISTRATIVELY"
    LOCATION_GPS = "LOCATION_GPS"


class GatewayIsmBand(str, enum.Enum):
    EU868 = "EU868"
    EU433 = "EU433"
    CN779 = "CN779"
    AS923 = "AS923"
    KR920 = "KR920"
    SG920 = "SG920"
    TW920 = "TW920"
    US915 = "US915"
    AU915 = "AU915"
    CN470 = "CN470"
    IN865 = "IN865"
    RU864 = "RU864"


class MachineqapiGatewayConnectionState(str, enum.Enum):
    NEVERCNX = "NEVERCNX"
    CNX = "CNX"
    DISC = "DISC"
    CNX_UNKNOWN = "CNX_UNKNOWN"


class MachineqapiGatewayHealthState(str, enum.Enum):
    INIT = "INIT"
    ACTIVE = "ACTIVE"
    BACKHAUL_CNX_ERROR = "BACKHAUL_CNX_ERROR"
    RF_ERROR = "RF_ERROR"
    HEALTH_UNKNOWN = "HEALTH_UNKNOWN"


class MachineqapiGatewayManufacturer(str, enum.Enum):
    UNKNOWN_MFR = "UNKNOWN_MFR"
    COMCAST = "COMCAST"
    TEKTELIC = "TEKTELIC"
    MULTITECH = "MULTITECH"


class InterfaceState(str, enum.Enum):
    IF_UNKNOWN = "IF_UNKNOWN"
    DOWN = "DOWN"
    UP_LINKDOWN = "UP_LINKDOWN"
    UP_NOSIGNAL = "UP_NOSIGNAL"
    UP_NOIP = "UP_NOIP"
    UP_NETWORKDOWN = "UP_NETWORKDOWN"
    UP_RUNNING = "UP_RUNNING"
    UP_RUNNING_USED = "UP_RUNNING_USED"


class InterfaceStatistics(BaseModelWithConfig):
    name: str
    state: InterfaceState
    type: str


class GatewayStatistics(BaseModelWithConfig):
    connection_state: MachineqapiGatewayConnectionState
    health_state: MachineqapiGatewayHealthState
    gps_sync_status: GatewayGpsSyncStatus
    time_sync_status: GatewayTimeSyncStatus
    last_reporting_time: datetime | None
    last_uplink_time: datetime | None
    last_downlink_time: datetime | None
    location_type: GatewayLocationType
    rf_region_id: str = Field(alias="RfRegionID")
    is_rx2_activated: bool = Field(alias="IsRX2Activated")
    ism_band: GatewayIsmBand
    last_geo_latitude: float
    last_geo_longitude: float
    last_geo_altitude: float
    software_version: str
    uplink_packet_per_hour: int
    downlink_packet_per_hour: int
    last_system_reboot: datetime | None
    interface_statistics: list[InterfaceStatistics]
    cpu_percent: int = Field(alias="CPUPercent")
    free_mem_kb: int = Field(alias="FreeMemKB")
    cell_rssi: int = Field(alias="CellRSSI")
    cell_provider: str
    wifi_ssid: str = Field(alias="WiFiSSID")
    radio_error: str
    tx_power: int
    VSWR: int
    last_geo_valid: bool
    secure_backhaul_enabled: bool
    secure_backhaul_active: bool
    model: str
    lrr_cnx: bool = Field(alias="LrrCNX")


class GatewayInstance(BaseModelWithConfig):
    id: str
    gateway_profile: str
    mac_address: str
    node_id: str
    name: str
    antenna_gain: str
    location_type: LocationType
    gps_enabled: bool = Field(alias="GPSEnabled")
    coordinates: Coordinates
    cellular_enabled: bool
    IMEI: str
    ICCID: str
    created_at: datetime
    updated_at: datetime
    updated_by: str
    manufacturer: MachineqapiGatewayManufacturer
    model: str
    statistics: GatewayStatistics | None
    rf_region: str


class GatewayCreate(BaseModelWithConfig):
    gateway_profile: str
    mac_address: str
    node_id: str
    name: str
    antenna_gain: str = "0"
    location_type: LocationType = LocationType.INDOOR
    gps_enabled: bool | None = Field(default=None, alias="GPSEnabled")
    coordinates: Coordinates
    cellular_enabled: bool | None = None
    IMEI: str | None = None
    ICCID: str | None = None


class GatewayCreateResponse(BaseModelWithConfig):
    id: str


class GatewayError(BaseModelWithConfig):
    response: bool


class GatewayPatch(BaseModelWithConfig):
    id: str
    name: str | None
    antenna_gain: str | None
    location_type: LocationType | None
    coordinates: Coordinates | None
    gateway_profile: str | None
    gps_enabled: bool | None = Field(default=None, alias="GPSEnabled")
    cellular_enabled: bool | None
    IMEI: str | None = None
    ICCID: str | None = None
    rf_region: str | None


class GatewayUpdate(BaseModelWithConfig):
    id: str
    name: str
    antenna_gain: str
    location_type: LocationType
    coordinates: Coordinates | None
    gateway_profile: str
    gps_enabled: bool | None = Field(default=None, alias="GPSEnabled")
    cellular_enabled: bool | None
    IMEI: str | None = None
    ICCID: str | None = None


class GatewayActivationInfo(BaseModelWithConfig):
    subscriber_id: str = Field(alias="subscriberId")
    activated: bool


class GatewayDevice(BaseModelWithConfig):
    name: str
    deveui: str
    statistics: str
    last_uplink: datetime


class GatewayDeviceResponse(BaseModelWithConfig):
    devices: list[GatewayDevice]


class GatewayEvent(BaseModelWithConfig):
    time: str
    field: GatewayEventField
    old_value: str
    new_value: str


class CreateGatewaysResponse(BaseModelWithConfig):
    response: bool
    mac_address: str
    error: str
    id: str


class GatewaysConnectionResponse(BaseModelWithConfig):
    never_connected: list[GatewayInstance]
    disconnected: list[GatewayInstance]
    connected: list[GatewayInstance]


class GatewaysHealthResponse(BaseModelWithConfig):
    initializing: list[GatewayInstance]
    connect_error: list[GatewayInstance]
    rf_error: list[GatewayInstance]
    active: list[GatewayInstance]


class MachineqapiGatewayResponse(BaseModelWithConfig):
    gateways: list[GatewayInstance]


class MachineqapiGetGatewayEventsResponse(BaseModelWithConfig):
    node_id: str = Field(alias="NodeID")
    events: list[GatewayEvent]
