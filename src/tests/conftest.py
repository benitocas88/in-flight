import pytest


@pytest.fixture
def webhook_schema_data():
    return {
        "webhook_type": "random-webhook_type",
        "webhook_code": "random-webhook_code",
        "link_id": "a6ddbef7-3a54-4122-a37d-829b2351fac5",
        "request_id": "669db10f70e3466483853c270b8f7309",
        "data": {},
    }
