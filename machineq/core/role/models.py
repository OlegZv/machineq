from machineq.core.shared.models import BaseModelWithConfig

from ..account.models import PermissionObject


class RoleCreate(BaseModelWithConfig):
    name: str
    device: PermissionObject | None = None
    user: PermissionObject | None = None
    gateway: PermissionObject | None = None
    users: list[str] | None = None
    applications: list[str] | None = None


class RoleCreateResponse(BaseModelWithConfig):
    id: str


class RoleError(BaseModelWithConfig):
    response: bool


class RoleInstance(BaseModelWithConfig):
    id: str
    name: str
    device: PermissionObject | None
    user: PermissionObject | None
    gateway: PermissionObject | None
    users: list[str]
    applications: list[str]


class RolePatch(BaseModelWithConfig):
    id: str
    name: str | None
    device: PermissionObject | None
    user: PermissionObject | None
    gateway: PermissionObject | None
    users: list[str] | None
    applications: list[str] | None


class RoleResponse(BaseModelWithConfig):
    roles: list[RoleInstance]


class RoleUpdate(BaseModelWithConfig):
    id: str
    name: str
    device: PermissionObject | None
    user: PermissionObject | None
    gateway: PermissionObject | None
    users: list[str] | None
    applications: list[str] | None
