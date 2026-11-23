from flight.orders.schemas import NotifyPaymentStatus
from flight.utils.validator import schema_validator


def test_schema_validator_validates_and_serializes_task_inputs():
    @schema_validator(NotifyPaymentStatus)
    def collect_inputs(**kwargs):
        return kwargs

    values = collect_inputs(
        meta={"request_id": "669db10f-70e3-4664-8385-3c270b8f7309"},
        receiver={"url": "https://example.com/webhook"},
        body={
            "request_id": "669db10f-70e3-4664-8385-3c270b8f7309",
            "data": {
                "order_id": "A-2023/01",
                "payment": {"authorization_code": None, "status": "rejected"},
                "created_at": 60,
            },
        },
    )

    assert values["meta"]["request_id"] == "669db10f70e3466483853c270b8f7309"
    assert values["receiver"]["url"] == "https://example.com/webhook"
    assert values["body"]["data"]["created_at"] == 60.0
