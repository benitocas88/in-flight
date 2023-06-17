from functools import wraps
from typing import Callable, Dict, Type

from marshmallow.schema import Schema

# from ooks.mixins.schemas import WebhookReceiverSchema
from structlog import get_logger

logger = get_logger(__name__)


def schema_validator(schema: Type[Schema]) -> Callable:
    def _validate(fxn: Callable) -> Callable:
        @wraps(fxn)
        def _task_validator(meta: Dict, receiver: Dict, body: Dict) -> Callable:
            """
            try:
                meta = MetaSchema().load(meta)
                receiver = WebhookReceiverSchema().load(receiver)
                body = schema().load(body)
            except ValidationError as exc:
                logger.error("schema_webhook_validator", message=exc.messages)
                raise exc
            else:
                return fxn(meta=meta, receiver=receiver, body=body)
            """

        return _task_validator

    return _validate
