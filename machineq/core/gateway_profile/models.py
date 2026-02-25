from machineq.core.shared.models import BaseModelWithConfig


class GatewayProfileInstance(BaseModelWithConfig):
    id: str
    name: str
    description: str


class GatewayProfileResponse(BaseModelWithConfig):
    gateway_profiles: list[GatewayProfileInstance]
