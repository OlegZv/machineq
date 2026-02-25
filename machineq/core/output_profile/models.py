from pydantic import Field

from machineq.core.shared.models import BaseModelWithConfig


class OutputProfileMQTTParams(BaseModelWithConfig):
    host: str
    username: str
    password: str
    topic: str
    SSL: bool | None = None
    client_id: str | None
    destination_id: str | None
    active: bool | None
    environment: str | None


class OutputProfileRestParams(BaseModelWithConfig):
    URL: str
    token_type: str | None
    token_value: str | None
    output_format: str
    destination_id: str | None
    active: bool | None
    environment: str | None


class OutputProfileAzureMQTTParams(BaseModelWithConfig):
    host: str
    shared_access_policy_name: str
    shared_access_key: str
    api_version: str
    output_format: str | None
    destination_id: str | None
    active: bool | None
    environment: str | None


class OutputProfileAWSParams(BaseModelWithConfig):
    endpoint: str
    x509_certificate: str
    private_key: str
    destination_id: str | None
    active: bool | None
    environment: str | None


class OutputProfileInstance(BaseModelWithConfig):
    id: str
    name: str
    mqtt_params: list[OutputProfileMQTTParams]
    rest_params: list[OutputProfileRestParams]
    azure_params: list[OutputProfileAzureMQTTParams]
    aws_params: list[OutputProfileAWSParams] = Field(alias="AWSParams")


class OutputProfileCreate(BaseModelWithConfig):
    name: str
    mqtt_params: list[OutputProfileMQTTParams] | None = None
    rest_params: list[OutputProfileRestParams] | None = None
    azure_params: list[OutputProfileAzureMQTTParams] | None = None
    aws_params: list[OutputProfileAWSParams] | None = Field(default=None, alias="AWSParams")


class OutputProfileCreateResponse(BaseModelWithConfig):
    id: str


class OutputProfileError(BaseModelWithConfig):
    response: bool


class OutputProfilePatch(BaseModelWithConfig):
    id: str
    name: str | None
    mqtt_params: list[OutputProfileMQTTParams] | None
    rest_params: list[OutputProfileRestParams] | None
    azure_params: list[OutputProfileAzureMQTTParams] | None
    aws_params: list[OutputProfileAWSParams] | None = Field(default=None, alias="AWSParams")


class OutputProfileResponse(BaseModelWithConfig):
    output_profiles: list[OutputProfileInstance]


class OutputProfileUpdate(BaseModelWithConfig):
    id: str
    name: str
    mqtt_params: list[OutputProfileMQTTParams] | None
    rest_params: list[OutputProfileRestParams] | None
    azure_params: list[OutputProfileAzureMQTTParams] | None
    aws_params: list[OutputProfileAWSParams] | None = Field(default=None, alias="AWSParams")


class OutputProfileDevicesResponse(BaseModelWithConfig):
    deveui: str
    response: bool
    error: str


class OutputProfileDevicesUpdate(BaseModelWithConfig):
    id: str
    devices: list[str] | None


class OutputProfileDevicesUpdateResponse(BaseModelWithConfig):
    responses: list[OutputProfileDevicesResponse]
