from functools import wraps
from typing import Callable, TypeVar, cast

from celery.app.task import Task
from requests.exceptions import HTTPError, Timeout
from typing_extensions import ParamSpec

from app import celery


class BaseTaskWithRetry(Task):  # noqa
    autoretry_for = (
        HTTPError,
        Timeout,
    )
    max_retries = 3
    retry_jitter = True
    retry_backoff = 5
    retry_backoff_max = 300


P = ParamSpec("P")
T = TypeVar("T")


def celery_task_with_retry(name: str) -> Callable:
    def wrapper_task(func: Callable[P, T]) -> Callable[P, T]:
        @celery.task(name=name, base=BaseTaskWithRetry)
        @wraps(func)
        def celery_task(*_: P.args, **kwargs: P.kwargs) -> T:
            meta = cast(dict, kwargs.get("meta"))
            webhook = cast(dict, kwargs.get("webhook"))
            return func(meta=meta, **webhook)  # type:ignore

        return celery_task

    return wrapper_task
