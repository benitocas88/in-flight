from typing import Dict, Tuple


def add_event_details(_: Tuple, __: Dict, event_dict: Dict) -> Dict:
    event_dict["evt.name"] = event_dict.get("event")

    outcome = event_dict.pop("outcome", None)
    if outcome:
        event_dict["evt.outcome"] = outcome.upper()

    return event_dict


def add_app_active_scope(_: Tuple, __: Dict, event_dict: Dict) -> Dict:
    event_dict["scope"] = "flight"
    return event_dict
