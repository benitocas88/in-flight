from pathlib import Path
from typing import List

from celery.app.base import Celery
from celery.app.task import Task
from flask.app import Flask

import flight
from flight.celery.settings import BaseCelerySettings

EXCLUDED_TASK_PACKAGES = {"celery", "logs", "mixins", "settings", "utils"}


def autodiscover_tasks() -> List[str]:
    package_path = Path(next(iter(flight.__path__)))
    task_modules = []

    for tasks_file in package_path.rglob("tasks.py"):
        relative_path = tasks_file.relative_to(package_path.parent)
        parts = relative_path.with_suffix("").parts

        if any(part in EXCLUDED_TASK_PACKAGES for part in parts):
            continue

        task_modules.append(".".join(parts))

    return task_modules


def make_celery(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.import_name, task_cls=FlaskTask)
    celery.config_from_object(BaseCelerySettings)
    celery.set_default()
    celery.autodiscover_tasks(autodiscover_tasks())
    app.extensions["celery"] = celery

    return celery
