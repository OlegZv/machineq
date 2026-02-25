from machineq.core.shared.models import BaseModelWithConfig


class ServiceProfileInstance(BaseModelWithConfig):
    id: str
    name: str
    description: str


class ServiceProfilesResponse(BaseModelWithConfig):
    service_profiles: list[ServiceProfileInstance]
