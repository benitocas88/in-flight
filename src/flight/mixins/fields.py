from uuid import UUID

from marshmallow import fields
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Range


class UUIDString(fields.UUID):
    def _deserialize(self, value, attr, data, **kwargs) -> str:  # type: ignore
        try:
            return str(UUID(value))
        except Exception as exc:
            raise ValidationError(str(exc)) from exc


class UUIDHex(fields.UUID):
    def _deserialize(self, value, attr, data, **kwargs) -> str:  # type: ignore
        try:
            return UUID(value).hex
        except Exception as exc:
            raise ValidationError(str(exc)) from exc


class StrictInteger(fields.Integer):
    def __init__(self, *, strict: bool = False, **kwargs):  # type: ignore
        self.strict = strict

        kwargs.update(
            required=True,
            validate=Range(min=0),
            allow_none=False,
            default=0,
        )

        super().__init__(**kwargs)
