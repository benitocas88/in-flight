from typing import Dict
from uuid import uuid4

from flight.mixins.fields import UUIDHex
from marshmallow import fields
from marshmallow.decorators import pre_load
from marshmallow.schema import Schema


class BodySchema(Schema):
    class Meta:
        ordered = True


class WebhookSchema(Schema):
    webhook_id = UUIDHex(required=True)
    request_id = UUIDHex(required=True)
    data = fields.Dict(required=True)

    class Meta:
        ordered = True

    @pre_load
    def make_webhook_id(self, data: Dict, **_: Dict) -> Dict:
        data["webhook_id"] = uuid4().hex
        return data
