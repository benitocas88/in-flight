import json
import os
from typing import List

from celery.app.base import Celery
from celery.app.task import Task
from flask.app import Flask
from flight.settings.celery.config import CeleryConfig


def autodiscover_tasks() -> List[str]:
    exclusions = ["logs", "mixins", "settings", "utils"]
    tasks = []
    for root, dirs, files in os.walk("flight"):
        roots = root.split("/")
        if not len(roots) == 2:
            continue

        if roots[-1] in exclusions:
            continue

        if "tasks.py" in files:
            tasks.append(root.replace("/", "."))

    return tasks


def make_celery(app: Flask) -> Celery:
    from ddtrace import config, patch

    patch(celery=True)
    config.celery["worker_service_name"] = "flight-worker"

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.config_from_object(CeleryConfig, namespace="CELERY_NS_FLIGHT")
    celery.set_default()
    celery.autodiscover_tasks(autodiscover_tasks())
    app.extensions["celery"] = celery

    return celery
