from functools import wraps
from typing import Any, Callable, Dict, TypeVar

from pydantic import BaseModel, ValidationError
from structlog import get_logger

from flight.mixins.metas import MetaSchema, ReceiverSchema

logger = get_logger(__name__)

Model = TypeVar("Model", bound=BaseModel)
Result = TypeVar("Result")


def schema_validator(
    schema: type[Model],
) -> Callable[[Callable[..., Result]], Callable[..., Result]]:
    def _validate(fxn: Callable[..., Result]) -> Callable[..., Result]:
        @wraps(fxn)
        def _task_validator(
            meta: Dict[str, Any],
            receiver: Dict[str, Any],
            body: Dict[str, Any],
        ) -> Result:
            try:
                validated_meta = MetaSchema.model_validate(meta)
                validated_receiver = ReceiverSchema.model_validate(receiver)
                validated_body = schema.model_validate(body)
            except ValidationError as exc:
                logger.error("schema_webhook_validator", errors=exc.errors(include_input=False))
                raise

            return fxn(
                meta=validated_meta.model_dump(mode="json"),
                receiver=validated_receiver.model_dump(mode="json"),
                body=validated_body.model_dump(mode="json"),
            )

        return _task_validator

    return _validate
