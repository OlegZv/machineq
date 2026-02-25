from machineq.core.shared.models import BaseModelWithConfig


class PermissionObject(BaseModelWithConfig):
    create: bool
    read: bool
    update: bool
    delete: bool


class SubscriberInfo(BaseModelWithConfig):
    id: str
    name: str
    address: str
    address2: str
    city: str
    state: str
    country: str
    postal_code: str


class UserInfo(BaseModelWithConfig):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    phone_number: str
    roles: list[str]


class UserInfoPatch(BaseModelWithConfig):
    email: str
    first_name: str
    last_name: str
    phone_number: str


class UserInfoUpdate(BaseModelWithConfig):
    email: str
    first_name: str
    last_name: str
    phone_number: str | None


class AccountError(BaseModelWithConfig):
    response: bool


class AccountPasswordReset(BaseModelWithConfig):
    current_password: str
    new_password: str


class AccountPermissionResponse(BaseModelWithConfig):
    device: PermissionObject
    gateway: PermissionObject
    user: PermissionObject
    subscriber_admin: PermissionObject
    network_operator: PermissionObject
    sys_admin: PermissionObject


class AccountResponse(BaseModelWithConfig):
    # User info is None if called with an application token.
    user_info: UserInfo | None
    subscriber_info: SubscriberInfo
