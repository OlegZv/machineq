from machineq.core.shared.models import BaseModelWithConfig


class CreateMulticastGroupRequest(BaseModelWithConfig):
    name: str
    multicast_deveui: str
    multicast_dev_addr: str
    group_type: str
    multicast_nwk_s_key: str
    multicast_app_s_key: str
    data_rate: int
    frequency: int
    ping_slot_period: int


class CreateMulticastGroupResponse(BaseModelWithConfig):
    response: bool


class UpdateMulticastGroupRequest(BaseModelWithConfig):
    multicast_deveui: str
    name: str
    data_rate: int
    frequency: int


class UpdateMulticastGroupResponse(BaseModelWithConfig):
    response: bool


class DeleteMulticastGroupResponse(BaseModelWithConfig):
    response: bool


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


class AddDevicesWithMulticastGroupRequest(BaseModelWithConfig):
    multicast_deveui: str
    devices: list[str]


class AddDevicesWithMulticastGroupResponse(BaseModelWithConfig):
    devices_added: list[str]
    devices_ignored: list[str]


class RemoveDevicesFromMulticastGroupRequest(BaseModelWithConfig):
    multicast_deveui: str
    devices: list[str]


class RemoveDevicesFromMulticastGroupResponse(BaseModelWithConfig):
    devices_removed: list[str]
    devices_ignored: list[str]


class AddGatewaysWithMulticastGroupRequest(BaseModelWithConfig):
    multicast_deveui: str
    gateways: list[str]


class AddGatewaysWithMulticastGroupResponse(BaseModelWithConfig):
    gateways_added: list[str]
    gateways_ignored: list[str]


class RemoveGatewaysFromMulticastGroupRequest(BaseModelWithConfig):
    multicast_deveui: str
    gateways: list[str]


class RemoveGatewaysFromMulticastGroupResponse(BaseModelWithConfig):
    gateways_removed: list[str]
    gateways_ignored: list[str]


class GetGatewaysByMulticastGroupResponse(BaseModelWithConfig):
    gateways: list[str]
