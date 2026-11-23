from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator


def _uuid_hex(value: object) -> str:
    try:
        return UUID(str(value)).hex
    except (TypeError, ValueError) as exc:
        raise ValueError("Input should be a valid UUID") from exc


UUIDHex = Annotated[str, BeforeValidator(_uuid_hex)]
