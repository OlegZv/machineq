from enum import Enum

from machineq.core.shared.models import BaseModelWithConfig


class MulticastGroupType(str, Enum):
    CLASS_C = "C"
    CLASS_B = "B"


class CreateMulticastGroupRequest(BaseModelWithConfig):
    name: str
    multicast_deveui: str
    multicast_dev_addr: str
    group_type: MulticastGroupType
    multicast_nwk_s_key: str
    multicast_app_s_key: str
    data_rate: int
    frequency: int
    """The frequency for multicast group in units of Hz."""
    ping_slot_period: int = 0
    """The pingslot period for multicast group. Required for ClassB, ignored for ClassC."""


class UpdateMulticastGroupRequest(BaseModelWithConfig):
    name: str
    data_rate: int
    frequency: int


class MulticastGroup(BaseModelWithConfig):
    name: str
    multicast_deveui: str
    multicast_dev_addr: str
    group_type: str
    data_rate: int
    frequency: int
    ping_slot_period: int


class GetMulticastGroupResponse(BaseModelWithConfig):
    multicast_group: MulticastGroup


class GetMulticastGroupsResponse(BaseModelWithConfig):
    multicast_groups: list[MulticastGroup]


class AddGatewaysWithMulticastGroupRequest(BaseModelWithConfig):
    gateways: list[str]


class AddGatewaysWithMulticastGroupResponse(BaseModelWithConfig):
    gateways_added: list[str]
    gateways_ignored: list[str]


class RemoveGatewaysFromMulticastGroupRequest(BaseModelWithConfig):
    gateways: list[str]


class RemoveGatewaysFromMulticastGroupResponse(BaseModelWithConfig):
    gateways_removed: list[str]
    gateways_ignored: list[str]


class GetGatewaysByMulticastGroupResponse(BaseModelWithConfig):
    gateways: list[str]
