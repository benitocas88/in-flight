from uuid import UUID

import pytest
from flight.mixins.metas import MetaSchema, ReceiverSchema
from flight.mixins.schemas import WebhookSchema
from flight.orders.schemas import NotifyPaymentStatus
from pydantic import ValidationError


def test_webhook_schema_generates_id_and_normalizes_request_id():
    webhook = WebhookSchema.model_validate(
        {
            "request_id": "669db10f-70e3-4664-8385-3c270b8f7309",
            "data": {},
        }
    )

    assert webhook.webhook_id == UUID(webhook.webhook_id).hex
    assert webhook.request_id == "669db10f70e3466483853c270b8f7309"


def test_webhook_schema_replaces_supplied_id():
    webhook = WebhookSchema.model_validate(
        {
            "webhook_id": "supplied-id",
            "request_id": "669db10f70e3466483853c270b8f7309",
            "data": {},
        }
    )

    assert webhook.webhook_id != "supplied-id"


def test_meta_schema_generates_request_id():
    meta = MetaSchema.model_validate({})

    assert meta.request_id == UUID(meta.request_id).hex


def test_meta_schema_generates_id_for_empty_value():
    meta = MetaSchema.model_validate({"request_id": ""})

    assert meta.request_id == UUID(meta.request_id).hex


def test_receiver_schema_requires_https():
    receiver = ReceiverSchema.model_validate({"url": "https://example.com/webhook"})

    assert receiver.url.scheme == "https"

    with pytest.raises(ValidationError):
        ReceiverSchema.model_validate({"url": "http://example.com/webhook"})


def test_notify_payment_status_validates_and_serializes_duration():
    webhook = NotifyPaymentStatus.model_validate(
        {
            "request_id": "669db10f70e3466483853c270b8f7309",
            "data": {
                "order_id": "A-2023/01",
                "payment": {"authorization_code": None, "status": "rejected"},
                "created_at": 60,
            },
        }
    )

    assert webhook.model_dump(mode="json")["data"]["created_at"] == 60.0


def test_notify_payment_status_rejects_invalid_status_and_short_duration():
    with pytest.raises(ValidationError):
        NotifyPaymentStatus.model_validate(
            {
                "request_id": "669db10f70e3466483853c270b8f7309",
                "data": {
                    "order_id": "A-2023/01",
                    "payment": {"authorization_code": None, "status": "pending"},
                    "created_at": 30,
                },
            }
        )
