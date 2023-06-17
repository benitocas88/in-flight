from typing import Any, Dict, MutableMapping, Tuple, cast

from flight.settings import base
from requests.exceptions import HTTPError, JSONDecodeError, Timeout
from requests.models import Response
from requests.sessions import Session
from structlog import get_logger

logger = get_logger(__name__)

__version__ = "1.0.0"


class HttpClient:
    url: str
    session: Session

    def __init__(self, meta: Dict, receiver: Dict):
        self.url = cast(str, receiver.get("url"))

        auth = {}
        if "auth" in receiver:
            sec = cast(dict, receiver.get("auth"))
            auth.update({sec["key"]: sec["value"]})

        request_id = cast(str, meta.get("request_id"))

        session = Session()
        session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": f"in-flight-webhooks ({__version__})",
                "X-Request-Id": request_id,
                **auth,
            }
        )

        session.hooks["response"].append(self.add_hook_response)
        self.session = session

    @staticmethod
    def __header_sanitizer(headers: MutableMapping) -> Dict:
        protected_keys = [
            "authorization",
            "token",
            "secret",
            "password",
            "authentication",
        ]
        return {k: ("*" * 6) if k.lower() in protected_keys else v for k, v in headers.items()}

    def add_hook_response(self, response: Response, *_: Tuple, **__: Dict) -> None:
        logger.info(
            "webhook_request_sent",
            headers=self.__header_sanitizer(response.request.headers),
            url=response.url,
            request_body=response.request.body,
            outcome="success" if 200 <= response.status_code <= 299 else "failure",
            elapsed_time=response.elapsed.total_seconds(),
        )

    def post(self, json: Dict) -> Tuple[bool, int]:
        try:
            logger.info("webhook_request_started")
            response = self.session.post(url=self.url, json=json, timeout=base.HTTP_REQUEST_TIMEOUT)
            response.raise_for_status()
        except (HTTPError, Timeout) as exc:
            logger.error("webhook_request_failed", exc_info=str(exc))
            raise exc
        else:
            try:
                json_response = response.json()
            except JSONDecodeError:
                json_response = None

            logger.info(
                "webhook_request_finished",
                status_code=response.status_code,
                json_response=json_response,
            )

            return True, response.status_code


def webhook_dispatcher(meta: Dict, receiver: Dict, body: Dict) -> Any:
    http = HttpClient(meta, receiver)
    return http.post(body)
