from logging import Filter, LogRecord
from typing import Dict

from structlog.contextvars import get_contextvars


class RequestIdFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        try:
            items: Dict = get_contextvars()
            request_id = items["request_id"]
            setattr(record, "request_id", request_id)
        except KeyError:
            pass
        return True
