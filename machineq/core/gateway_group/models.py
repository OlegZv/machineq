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
    name: str | None = None
    gateway_list: list[str] | None = None


class GatewayGroupResponse(BaseModelWithConfig):
    gateway_groups: list[GatewayGroupInstance]


class GatewayGroupUpdate(BaseModelWithConfig):
    name: str
    gateway_list: list[str] | None
