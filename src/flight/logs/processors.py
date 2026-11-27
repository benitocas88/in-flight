from structlog.typing import EventDict, WrappedLogger


def add_event_details(
    _: WrappedLogger,
    __: str,
    event_dict: EventDict,
) -> EventDict:
    event_dict["evt.name"] = event_dict.get("event")
    return event_dict
