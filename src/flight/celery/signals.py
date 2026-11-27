from celery import signals
from celery.app.task import Task
from pydantic import ValidationError
from structlog import get_logger
from structlog.contextvars import bind_contextvars, clear_contextvars

from flight.logs.logger import make_structlog
from flight.mixins.metas import MetaSchema

logger = get_logger(__name__)


@signals.task_prerun.connect
def on_task_prerun(
    sender: Task,
    task_id: str,
    kwargs: dict[str, object],
    **_: object,
) -> None:
    clear_contextvars()
    bind_contextvars(task_id=task_id, task_name=sender.name)

    try:
        meta = MetaSchema.model_validate(kwargs.get("meta", {}))
        bind_contextvars(**meta.model_dump(mode="json"))
    except ValidationError as exc:
        logger.warning("meta_validation", errors=exc.errors(include_input=False))


@signals.task_postrun.connect
def on_task_postrun(*_: tuple[object, ...], **__: object) -> None:
    clear_contextvars()


@signals.after_setup_logger.connect
def on_after_setup_logger(*_: tuple[object, ...], **__: object) -> None:
    make_structlog()
