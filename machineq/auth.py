from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from httpx import Client, Response

GRACE_PERIOD_S = 5


class MqApiEnvironment(str, Enum):
    PROD = "prod"
    DEV = "dev"
    PREVIEW = "preview"


# authentication exception that will capture text error and optional status code
class AuthenticationException(Exception):
    def __init__(self, res: Response | None = None):
        if res is not None:
            if res.status_code == 429:
                message = "Failed to get an access token. Rate limit exceeded. Please try again later."
            else:
                message = f"Failed to get an access token. Code: {res.status_code}. {res.text}"
        self.message: str = message
        self.request: Response | None = res
        super().__init__(self.message)


@dataclass
class MqAuth:
    client_id: str
    client_secret: str
    client: Client = field(default_factory=lambda: Client())
    env: MqApiEnvironment = MqApiEnvironment.PROD

    expires_at: datetime = field(default_factory=lambda: datetime.now())
    refresh_token: str = ""
    id_token: str = ""
    _token: str = ""

    def __post_init__(self):
        self.client.headers.update({"User-Agent": "MQAPI-py/1.0"})

    @property
    def env_str(self):
        return f".{self.env}" if self.env != MqApiEnvironment.PROD else ""

    @property
    def oauth_host(self):
        return f"https://identity{self.env_str}.machineq.net/oauth"

    @property
    def token_url(self):
        return f"{self.oauth_host}/token"

    def refresh(self):
        auth_params: dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        res = self.client.post(
            self.token_url,
            timeout=10,
            data=auth_params,
        )
        if res.status_code != 200:
            raise AuthenticationException(res)
        creds = res.json()
        self._token = creds["access_token"]
        self.expires_at = datetime.now() + timedelta(seconds=creds["expires_in"])

    @property
    def token(self) -> str:
        if not self._token or (self.expires_at < datetime.now() + timedelta(seconds=GRACE_PERIOD_S)):
            self.refresh()
        if not self._token:
            raise AuthenticationException()
        return self._token
