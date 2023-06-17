from logging.config import dictConfig
from typing import Any

import structlog
from flight.logs.processors import add_event_details, add_app_active_scope
from flight.utils.environments import Environment


def make_structlog(logfile: Any) -> None:
    pre_chain = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.StackInfoRenderer(),
    ]

    post_chain = [
        add_event_details,
        add_app_active_scope,
    ]

    if not Environment.app_env_production():
        processors = pre_chain + post_chain
        processor = structlog.processors.JSONRenderer()
    else:
        processors = pre_chain + [structlog.processors.ExceptionPrettyPrinter()] + post_chain
        processor = structlog.dev.ConsoleRenderer()  # type: ignore

    processors.append(processor)

    configs = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "stdout": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": processor,
                "foreign_pre_chain": pre_chain,
            }
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
            }
        },
        "loggers": {
            "celery": {
                "handlers": ["default"],
                "level": logfile,
                "propagate": False,
            },
            "pydig.resolver": {
               "handlers": ["null"],
               "propagate": False,
            },
        },
    }

    dictConfig(configs)
    processors = processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter]
    structlog.configure(
        processors=processors,  # type: ignore
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,  # type: ignore
        cache_logger_on_first_use=True,
    )
