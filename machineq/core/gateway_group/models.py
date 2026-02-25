from machineq.core.shared.models import BaseModelWithConfig

from ..gateway.models import GatewayInstance


class GatewayGroupCreate(BaseModelWithConfig):
    name: str
    gateway_list: list[str] | None


class GatewayGroupCreateResponse(BaseModelWithConfig):
    id: str


class GatewayGroupError(BaseModelWithConfig):
    response: bool


class GatewayGroupInstance(BaseModelWithConfig):
    id: str
    name: str
    gateway_list: list[str]
    gateways: list[GatewayInstance]


class GatewayGroupPatch(BaseModelWithConfig):
    id: str
    name: str | None
    gateway_list: list[str] | None


class GatewayGroupResponse(BaseModelWithConfig):
    gateway_groups: list[GatewayGroupInstance]


class GatewayGroupUpdate(BaseModelWithConfig):
    id: str
    name: str
    gateway_list: list[str] | None
