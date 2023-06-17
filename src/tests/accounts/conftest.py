from unittest.mock import ANY

import pytest


@pytest.fixture
def account_recurrent_schema():
    return {
        "link_id": "a6ddbef7-3a54-4122-a37d-829b2351fac5",
        "request_id": "669db10f70e3466483853c270b8f7309",
        "data": {"new_accounts": 10},
    }


@pytest.fixture
def account_recurrent_expected_schema():
    return {
        "webhook_id": ANY,
        "webhook_type": "ACCOUNTS",
        "webhook_code": "new_accounts_available",
        "link_id": "a6ddbef7-3a54-4122-a37d-829b2351fac5",
        "request_id": "669db10f70e3466483853c270b8f7309",
        "data": {"new_accounts": 10},
    }
