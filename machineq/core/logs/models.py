import enum
from datetime import datetime
from typing import Any

from pydantic import Field

from machineq.core.shared.models import BaseModelWithConfig


class StreamFilter(str, enum.Enum):
    NOSTREAMFILTER = "NOSTREAMFILTER"
    UPSTREAM = "UPSTREAM"
    DOWNSTREAM = "DOWNSTREAM"


class MessageTypeFilter(str, enum.Enum):
    NOMESSAGETYPEFILTER = "NOMESSAGETYPEFILTER"
    MAC = "MAC"
    MACDATA = "MACDATA"
    DATA = "DATA"
    NONE = "NONE"


class LateFilter(str, enum.Enum):
    NOLATEFILTER = "NOLATEFILTER"
    LATEFALSE = "LATEFALSE"
    LATETRUE = "LATETRUE"


class ActivationFilter(str, enum.Enum):
    NOACTIVATIONFILTER = "NOACTIVATIONFILTER"
    JOINREQUEST = "JOINREQUEST"
    JOINACCEPT = "JOINACCEPT"


class AckFilter(str, enum.Enum):
    NOACKFILTER = "NOACKFILTER"
    ACKFALSE = "ACKFALSE"
    ACKTRUE = "ACKTRUE"


class LogFrameFilter(BaseModelWithConfig):
    stream: list[StreamFilter]
    message_type: list[MessageTypeFilter]
    late: list[LateFilter]
    activation: list[ActivationFilter]
    ack: list[AckFilter]


class GatewayList(BaseModelWithConfig):
    gateway: str
    RSSI: str
    SNR: str
    ESP: str
    time: str
    unowned: bool
    subscriber_id: str = Field(alias="SubscriberID")
    gateway_node_id: str = Field(alias="GatewayNodeID")


class LogInstance(BaseModelWithConfig):
    timestamp: datetime
    deveui: str
    dev_addr: str
    fport: str
    f_cnt: str
    message_type: str
    message_type_text: str
    payload_hex: str
    mic_hex: str = Field(alias="MICHex")
    primary_gateway_rssi: str = Field(alias="PrimaryGatewayRSSI")
    primary_gateway_snr: str = Field(alias="PrimaryGatewaySNR")
    primary_gateway_e_s_p: str
    spreading_factor: str
    airtime: str
    sub_band: str
    channel: str
    gateway_id: str = Field(alias="GatewayID")
    gateway_latitude: str = Field(alias="GatewayLatitide")
    gateway_longitude: str
    gateway_count: str
    gateway_list: list[GatewayList]
    device_latitude: str
    device_longitude: str
    device_location_radius: str
    mac_commands: str
    decoded_mac_commands: list[str]
    adr_bit: str = Field(alias="ADRbit")
    adr_ack_req: str = Field(alias="ADRAckReq")
    ack_requested: str = Field(alias="AckRequested")
    ack_bit: str = Field(alias="ACKbit")
    f_pending: str
    late: str
    dev_nonce: str
    join_eui: str = Field(alias="JoinEUI")
    gateway_unowned: bool
    gateway_subscriber_id: str = ""  # possibly deprecated?
    gateway_node_id: str = Field(alias="GatewayNodeID")
    """Could be "Not Owned" or the NodeID"""
    payload_decoded: dict[str, Any] | None = Field(default_factory=dict)
    multicast: bool = False


class LogResponse(BaseModelWithConfig):
    logs: list[LogInstance]
