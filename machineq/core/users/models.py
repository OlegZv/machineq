from machineq.core.shared.models import BaseModelWithConfig


class UserCreate(BaseModelWithConfig):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    roles: list[str] | None = None
    """If left blank(None), the user will be created without roles. Currently reflected as
    an array with an empty string in it ([""])"""


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
    """An empty roles set is represented as an array with an empty string in it ([""])"""
    admin_roles: list[str]
    subscriber_id: str


class UserPatch(BaseModelWithConfig):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    password: str | None = None
    roles: list[str] | None = None


class UserResponse(BaseModelWithConfig):
    users: list[UserInstance]


class UserUpdate(BaseModelWithConfig):
    email: str
    first_name: str
    last_name: str
    phone_number: str
    password: str
    roles: list[str] | None
