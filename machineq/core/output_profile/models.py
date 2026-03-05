from enum import Enum

from pydantic import Field

from machineq.core.shared.models import BaseModelWithConfig


class OutputProfileEnvironment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


class AzureOutputFormat(str, Enum):
    RAW = "raw"
    AZURE = "azure"


class CommonOuputProfileParams(BaseModelWithConfig):
    destination_id: str | None = None
    """The unique destination identifier assigned by the MQ APIs after creation"""
    active: bool | None = None
    """Defaults to true if not set"""
    environment: OutputProfileEnvironment | None = None
    """The deployment environment of the destination. Indicates the criticality of the delivered messages
    and ensures that the MachineQ Engineering and Operations teams provide the appropriate level of support."""


class OutputProfileMQTTParams(CommonOuputProfileParams):
    host: str
    """The MQTT hostname including the port (E.g., `machineq-dev.mqtt.net:8883`). Must be a valid hostname
    for a URL and not include a scheme (like `mqtt://` or `tcps://`). Note: some ports are reserved.
    Please refer to [this Support Article article](https://support.machineq.com/s/article/Adding-an-Output-Profile-from-the-MQ-APIs) for more information."""
    username: str
    password: str
    topic: str
    """MQTT Topic (${DEVEUI} and ${FPORT} used as replacement variables)"""
    SSL: bool | None = None
    client_id: str | None = None
    """The custom client id to be used (${DEVEUI} and ${FPORT} used as replacement variables)."""


class OutputProfileRestParams(CommonOuputProfileParams):
    url: str = Field(serialization_alias="URL", validation_alias="URL")
    """The full URL to a REST service. Must be a valid HTTP URL that contains a scheme and an optional port (E.g., https://machineq.dev.net:6565)
    Note: some port numbers are reserved.
    Please refer to [this Support Article](https://support.machineq.com/s/article/Adding-an-Output-Profile-from-the-MQ-APIs) for more information."""
    token_type: str | None = None
    token_value: str | None = None
    output_format: str = "extended"


class OutputProfileAzureMQTTParams(CommonOuputProfileParams):
    host: str
    """The IoT Hub hostname. Must be a valid URL in the form '{hubname}.azure-devices.net' and must not contain a scheme.
    Specifying a port has been deprecated. The hostname for new destinations should not include a port."""
    shared_access_policy_name: str
    """The shared access policy name with Device access enabled."""
    shared_access_key: str
    api_version: str
    """The API Version which the latest is currently 2021-10-01. Previously 2021-04-12 and 2016-11-14."""
    output_format: AzureOutputFormat = AzureOutputFormat.RAW
    """Azure is the IoT Hub common Device to Cloud (D2C) format."""


class OutputProfileAWSParams(CommonOuputProfileParams):
    endpoint: str
    """The IoT Core endpoint. Must be a valid URL in the form '{account-specific-prefix}.iot.{aws-region}.amazonaws.com'
    and must not contain a port or scheme. (E.g., a3fhmgkt5lz2ij.iot.us-east-1.amazonaws.com)"""
    x509_certificate: str = Field(serialization_alias="x509Certificate", validation_alias="x509Certificate")
    """The x509 certificate pem file. Note: You'll need to replace newlines with `\n.`"""
    private_key: str
    """The x509 private key. Note: You'll need to replace newlines with `\n.`"""


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
    name: str | None = None
    mqtt_params: list[OutputProfileMQTTParams] | None = None
    rest_params: list[OutputProfileRestParams] | None = None
    azure_params: list[OutputProfileAzureMQTTParams] | None = None
    aws_params: list[OutputProfileAWSParams] | None = Field(default=None, alias="AWSParams")


class OutputProfileResponse(BaseModelWithConfig):
    output_profiles: list[OutputProfileInstance]


class OutputProfileUpdate(BaseModelWithConfig):
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
    devices: list[str] | None


class OutputProfileDevicesUpdateResponse(BaseModelWithConfig):
    responses: list[OutputProfileDevicesResponse]
