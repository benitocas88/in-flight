from datetime import timedelta
from typing import Literal

from pydantic import Field

from flight.mixins.schemas import BodySchema, WebhookSchema


class PaymentSchema(BodySchema):
    authorization_code: str | None
    status: Literal["rejected", "refunded", "completed"]


class StatusSchema(BodySchema):
    order_id: str
    payment: PaymentSchema
    created_at: timedelta | None = Field(ge=timedelta(seconds=60))


class NotifyPaymentStatus(WebhookSchema):
    data: StatusSchema
