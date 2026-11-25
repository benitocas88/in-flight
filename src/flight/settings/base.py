import builtins
from os import environ
from typing import TypeVar, cast

from pydantic import TypeAdapter

Value = TypeVar("Value")
_MISSING = object()
_STR_ADAPTER = TypeAdapter(str)
_INT_ADAPTER = TypeAdapter(int)
_BOOL_ADAPTER = TypeAdapter(bool)


def _read(name: str, adapter: TypeAdapter[Value], default: object) -> Value:
    value = environ.get(name)
    if value is None:
        if default is _MISSING:
            raise ValueError(f'Environment variable "{name}" not set')
        return cast(Value, default)
    return adapter.validate_python(value)


class Env:
    def str(self, name: builtins.str, default: builtins.str | object = _MISSING) -> builtins.str:
        return _read(name, _STR_ADAPTER, default)

    def int(self, name: builtins.str, default: int | object = _MISSING) -> int:
        return _read(name, _INT_ADAPTER, default)

    def bool(self, name: builtins.str, default: bool | object = _MISSING) -> bool:
        return _read(name, _BOOL_ADAPTER, default)


env = Env()

SECRET_KEY = env.str("SECRET_KEY")

HTTP_REQUEST_TIMEOUT = env.int("HTTP_REQUEST_TIMEOUT", default=60)
