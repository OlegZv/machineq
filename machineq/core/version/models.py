from machineq.core.shared.models import BaseModelWithConfig


class VersionResponse(BaseModelWithConfig):
    semantic: str
    major: str
    minor: str
    patch: str
    build_time: str
