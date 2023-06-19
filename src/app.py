import os
from typing import Any, Dict, Tuple

from celery import signals
from celery.app.task import Task
from flask.app import Flask
from flight.logs.logger import make_structlog
from flight.mixins.metas import MetaSchema
from flight.settings.base import env
from flight.settings.celery.app import make_celery
from marshmallow.exceptions import ValidationError
from structlog import get_logger
from structlog.contextvars import bind_contextvars, clear_contextvars

logger = get_logger(__name__)

conf = os.path.join(
    os.path.dirname(__file__),
    "flight",
    "settings",
    env.str("ENV_FILENAME"),
)

app = Flask(__name__)
app.config.from_pyfile(conf)

celery = make_celery(app)

@signals.task_prerun.connect
def on_task_prerun(task: Task, *_: Tuple, **kwargs: Dict) -> None:
    binder = {"task_name": task.name}
    sqs_meta = kwargs.get("kwargs", {}).get("meta", {})

    try:
        meta = MetaSchema().load(sqs_meta)
        binder.update(**meta)
    except ValidationError as exc:
        logger.warning("meta_validation", message=exc.messages)

    clear_contextvars()
    bind_contextvars(**binder)


@signals.after_setup_logger.connect
def on_after_setup_logger(*_: Tuple, **__: Dict) -> None:
    make_structlog()


@app.cli.command("test")
def test():
    import time
    while True:
        print("message sent...")
        celery.send_task(
            "orders.notify_payment_status",
            kwargs={
                "meta": {},
                "webhook": {
                    "receiver": {},
                    "body": {}
                }
            }
        )
        time.sleep(7)
