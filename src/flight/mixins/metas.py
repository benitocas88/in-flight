from uuid import uuid4

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, field_validator, model_validator
from structlog import get_logger

from flight.mixins.fields import UUIDHex

logger = get_logger(__name__)


class MetaSchema(BaseModel):
    request_id: UUIDHex = Field(default_factory=lambda: uuid4().hex)

    @model_validator(mode="before")
    @classmethod
    def generate_request_id(cls, values):
        if isinstance(values, dict) and not values.get("request_id"):
            return {**values, "request_id": uuid4().hex}
        return values


class AuthSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    value: str


class ReceiverSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: AnyUrl
    auth: AuthSchema | None = None

    @field_validator("url")
    @classmethod
    def require_https(cls, value: AnyUrl) -> AnyUrl:
        if value.scheme != "https":
            raise ValueError("URL must use HTTPS")
        return value
