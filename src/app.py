import os
from typing import Dict, Tuple
from uuid import uuid4

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
def test() -> None:
    import time

    while True:
        request_id = uuid4().hex
        celery.send_task(
            "orders.notify_payment_status",
            kwargs={
                "meta": {"request_id": request_id},
                "webhook": {
                    "receiver": {
                        "url": "https://webhook.site/92a71e0f-b81b-4f62-b8ab-2822c350759d",
                        "auth": {
                            "key": "Bearer",
                            "value": (
                                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
                                "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
                            ),
                        },
                    },
                    "body": {
                        "data": {
                            "order_id": "A-2023/01",
                            "payment": {"authorization_code": None, "status": "rejected"},
                            "created_at": 1687737170,
                        },
                    },
                },
            },
        )
        print("message sent...")
        time.sleep(7)
