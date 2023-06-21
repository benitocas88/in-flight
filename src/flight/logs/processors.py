from typing import Dict, Tuple


def add_event_details(_: Tuple, __: Dict, event_dict: Dict) -> Dict:
    event_dict["evt.name"] = event_dict.get("event")
    return event_dict


def add_tracing_details(_: Tuple, __: Dict, event_dict: Dict) -> Dict:
    try:
        from ddtrace import tracer

        context = tracer.get_log_correlation_context()

        event_dict["dd.trace_id"] = context["trace_id"]
        event_dict["dd.span_id"] = context["span_id"]
        event_dict["dd.env"] = context["env"]
        event_dict["dd.service"] = context["service"]
        if context.get("version"):
            event_dict["dd.version"] = context["version"]
    except ModuleNotFoundError:
        pass
    finally:
        return event_dict
