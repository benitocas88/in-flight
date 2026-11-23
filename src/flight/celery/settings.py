from kombu.entity import Queue

from flight.settings.base import env


class BaseCelerySettings:
    """Base settings shared by Celery workers and tasks."""

    broker_url = env.str("BROKER_URL")
    broker_connection_retry_on_startup = True
    broker_transport_options = {
        "region": env.str("AWS_SQS_REGION_NAME", default="us-east-2"),
        "is_secure": env.bool("AWS_SQS_TRANSPORT_SECURE", default=True),
    }

    timezone = "UTC"
    enable_utc = True
    task_serializer = "json"
    accept_content = ["json"]

    worker_concurrency = 4
    worker_prefetch_multiplier = 1
    worker_max_tasks_per_child = 6

    task_default_queue = env.str("DEFAULT_QUEUE_NAME", default="in-flight")
    task_default_rate_limit = "60/s"
    task_queues = (Queue(task_default_queue),)
    task_create_missing_queues = False
    task_ignore_result = True
    task_acks_late = True
    task_track_started = True
    task_reject_on_worker_lost = True

    task_annotations = {
        "*": {
            "max_retries": 3,
            "retry_backoff": 5,
            "retry_backoff_max": 300,
            "retry_jitter": True,
            "soft_time_limit": 300,
            "time_limit": 360,
        }
    }
