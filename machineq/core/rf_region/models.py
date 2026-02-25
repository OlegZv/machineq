from machineq.core.shared.models import BaseModelWithConfig


class RFRegionInstance(BaseModelWithConfig):
    id: str
    name: str
    gateway_models: list[str]


class ListRFRegionsResponse(BaseModelWithConfig):
    rf_regions: list[RFRegionInstance]
