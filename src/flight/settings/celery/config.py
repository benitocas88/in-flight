from flight.settings.base import env
from flight.settings.celery.backends.s3 import S3Backend
from flight.settings.celery.brokers.sqs import SQSBroker
from kombu.entity import Queue


class CeleryConfig(SQSBroker, S3Backend):
    broker_url = env.str("BROKER_URL")

    timezone = "UTC"
    task_serializer = "json"
    result_serializer = "json"
    accept_content = ["json"]
    worker_concurrency = 8
    enable_utc = True

    task_default_queue = env.str("DEFAULT_QUEUE", default="in-flight")
    task_default_rate_limit = "60/s"
    task_queues = (Queue(task_default_queue),)
    task_ignore_result = True
    task_store_errors_even_if_ignored = True
    task_acks_late = True
    task_track_started = True
    task_create_missing_queues = False
