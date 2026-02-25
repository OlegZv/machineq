from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal


def alias_generator(snake: str) -> str:
    """Convert snake_case to PascalCase, with special handling for common abbreviations."""
    general = to_pascal(snake)
    if general.lower().endswith("eui"):
        return general[:-3] + "EUI"
    if general.lower().endswith("esp"):
        return general[:-3] + "ESP"
    if general.lower().endswith("snr"):
        return general[:-3] + "SNR"
    if general.lower().endswith("rssi"):
        return general[:-4] + "RSSI"
    return general


class BaseModelWithConfig(BaseModel):
    """Base model with common configuration for all models.
    Most of the time this config will be able to handle serializetion and deserialization
    for all models. Sometimes the alias would be different and can be overridden per field.
    For exampke, deveui is mostly DevEUI."""

    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True, serialize_by_alias=True, alias_generator=alias_generator
    )


# many APIs in case of success return just {"Response": true}
class CommonOKResponse(BaseModelWithConfig):
    response: bool
