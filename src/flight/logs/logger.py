from logging.config import dictConfig

import structlog
from flight.logs.processors import add_event_details, add_tracing_details
from flight.utils.environments import Environment


def make_structlog() -> None:
    pre_chain = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    post_chain = [
        add_tracing_details,
        add_event_details,
    ]

    if Environment.app_env_production():
        processors = pre_chain + post_chain
        processor = structlog.processors.JSONRenderer()
    else:
        processors = pre_chain + [structlog.processors.ExceptionPrettyPrinter()] + post_chain
        processor = structlog.dev.ConsoleRenderer()

    processors.append(processor)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "stdout": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "foreign_pre_chain": pre_chain,
                    "processor": processor,
                },
            },
            "filters": {
                "request_id": {
                    "()": "flight.logs.filters.RequestIdFilter",
                }
            },
            "handlers": {
                "null": {"class": "logging.NullHandler"},
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "stdout",
                    "filters": ["request_id"],
                },
            },
            "loggers": {
                "celery": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )

    structlog.configure_once(
        processors=processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,  # type: ignore
        cache_logger_on_first_use=True,
    )
