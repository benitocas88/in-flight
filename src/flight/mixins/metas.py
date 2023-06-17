from typing import Dict
from uuid import uuid4

from flight.mixins.fields import UUIDHex
from marshmallow import fields, validate
from marshmallow.decorators import pre_load
from marshmallow.schema import Schema

from structlog import get_logger

logger = get_logger(__name__)


class MetaSchema(Schema):
    request_id = UUIDHex(required=False)

    @pre_load
    def make_request_id(self, data: Dict, **_: Dict) -> Dict:
        if not data.get("request_id"):
            request_id = uuid4().hex
            data["request_id"] = request_id
            logger.info("request_id_missed", message=f"request_id not provided, automatic generated: {request_id}.")
        return data


class AuthSchema(Schema):
    key = fields.String(required=True)
    value = fields.String(required=True)


class ReceiverSchema(Schema):
    url = fields.Url(
        validate=validate.URL(schemes=["https"], require_tld=True, relative=False),
        required=True,
        allow_none=False,
    )
    auth = fields.Nested(AuthSchema(), required=False)
