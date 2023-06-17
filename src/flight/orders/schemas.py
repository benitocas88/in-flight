from flight.mixins.schemas import BodySchema, WebhookSchema
from marshmallow import fields, validate

PAYMENT_STATUS_ALLOWED = [
    "rejected",
    "refunded",
    "completed",
]


class StatusSchema(BodySchema):
    order_id = fields.String(required=True, allow_none=False)
    status = fields.String(
        required=True,
        validate=validate.ContainsOnly(PAYMENT_STATUS_ALLOWED),
        allow_none=False,
    )
    created_at_timestamp = fields.TimeDelta(
        precision="seconds", required=True, allow_none=True, validate=[validate.Range(min=60)]
    )


class NotifyPaymentStatus(WebhookSchema):
    data = fields.Nested(StatusSchema(), required=True)
