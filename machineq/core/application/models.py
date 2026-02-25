from machineq.core.shared.models import BaseModelWithConfig


class ApplicationCreate(BaseModelWithConfig):
    name: str
    roles: list[str] | None


class ApplicationCreateResponse(BaseModelWithConfig):
    id: str
    name: str
    UUID: str
    client_secret: str


class ApplicationInstance(BaseModelWithConfig):
    id: str
    name: str
    UUID: str
    roles: list[str]
    subscriber_id: str


class ApplicationPatch(BaseModelWithConfig):
    name: str | None = None
    roles: list[str] | None = None


class ApplicationResponse(BaseModelWithConfig):
    applications: list[ApplicationInstance]


class ApplicationUpdate(BaseModelWithConfig):
    name: str
    roles: list[str] | None


class RefreshApplicationResponse(BaseModelWithConfig):
    client_secret: str
