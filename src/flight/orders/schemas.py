from flight.mixins.schemas import BodySchema, WebhookSchema
from marshmallow import Schema, fields
from marshmallow.validate import ContainsOnly, Range

PAYMENT_STATUS_ALLOWED = [
    "rejected",
    "refunded",
    "completed",
]


class PaymentSchema(Schema):
    authorization_code = fields.String(required=True, allow_none=True)
    status = fields.String(required=True, validate=ContainsOnly(PAYMENT_STATUS_ALLOWED))


class StatusSchema(BodySchema):
    order_id = fields.String(required=True, allow_none=False)
    payment = fields.Nested(PaymentSchema(), required=True)
    created_at = fields.TimeDelta(
        precision="seconds",
        required=True,
        allow_none=True,
        validate=[Range(min=60)],
    )


class NotifyPaymentStatus(WebhookSchema):
    data = fields.Nested(StatusSchema(), required=True)
