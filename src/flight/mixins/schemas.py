from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from flight.mixins.fields import UUIDHex


class BodySchema(BaseModel):
    model_config = ConfigDict(extra="forbid", ser_json_timedelta="float")


class WebhookSchema(BodySchema):
    webhook_id: str = Field(default_factory=lambda: uuid4().hex)
    request_id: UUIDHex
    data: dict

    @model_validator(mode="before")
    @classmethod
    def generate_webhook_id(cls, values):
        if isinstance(values, dict):
            return {**values, "webhook_id": uuid4().hex}
        return values
