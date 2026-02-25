from machineq.core.shared.models import BaseModelWithConfig


class UserCreate(BaseModelWithConfig):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    roles: list[str] | None = None


class UserCreateResponse(BaseModelWithConfig):
    id: str


class UserError(BaseModelWithConfig):
    response: bool


class UserInstance(BaseModelWithConfig):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password_hash: str
    roles: list[str]
    admin_roles: list[str]
    subscriber_id: str


class UserPatch(BaseModelWithConfig):
    id: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    roles: list[str]


class UserResponse(BaseModelWithConfig):
    users: list[UserInstance]


class UserUpdate(BaseModelWithConfig):
    id: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    roles: list[str] | None
