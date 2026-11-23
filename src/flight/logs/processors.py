from typing import Dict, Tuple


def add_event_details(_: Tuple, __: Dict, event_dict: Dict) -> Dict:
    event_dict["evt.name"] = event_dict.get("event")
    return event_dict
