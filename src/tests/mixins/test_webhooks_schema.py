from unittest.mock import ANY

import pytest
from flight.mixins.schemas import BaseWebhookSchema
from marshmallow.exceptions import ValidationError


class TestWebhookSchema:
    @pytest.fixture
    def webhook_schema(self):
        return BaseWebhookSchema()

    def test_base_webhook_schema(self, webhook_schema, webhook_schema_data):
        schema_loaded = webhook_schema.load(webhook_schema_data)
        assert schema_loaded == {
            "webhook_id": ANY,
            "webhook_type": "random-webhook_type",
            "webhook_code": "random-webhook_code",
            "link_id": "a6ddbef7-3a54-4122-a37d-829b2351fac5",
            "request_id": "669db10f70e3466483853c270b8f7309",
            "data": {},
        }

    @pytest.mark.parametrize(
        "test_field_name",
        [
            "link_id",
            "request_id",
            "data",
        ],
    )
    def test_base_webhook_raise_errors_when_missing_data(
        self, webhook_schema, webhook_schema_data, test_field_name
    ):
        webhook_schema_data.pop(test_field_name)

        with pytest.raises(expected_exception=ValidationError) as exc:
            webhook_schema.load(webhook_schema_data)

        assert exc.value.messages[test_field_name] == ["Missing data for required field."]

    def test_raise_error_when_unknown_fields_are_there(self):
        pass

    def test_create_webhook_id_even_comes_in_payload(self):
        pass
