import json
from time import perf_counter
from typing import Any, Dict, MutableMapping, Tuple, cast

from httpx import Client, HTTPStatusError, Response, TimeoutException
from structlog import get_logger

from flight.settings import base

logger = get_logger(__name__)

__version__ = "1.0.0"


class HttpClient:
    url: str
    client: Client

    def __init__(self, meta: Dict, receiver: Dict):
        self.url = cast(str, receiver.get("url"))

        auth = {}
        if "auth" in receiver:
            sec = cast(dict, receiver.get("auth"))
            auth.update({sec["key"]: sec["value"]})

        request_id = cast(str, meta.get("request_id"))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"in-flight-webhooks ({__version__})",
            "X-Request-Id": request_id,
            **auth,
        }

        self.client = Client(headers=headers)

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

    def add_hook_response(self, response: Response, elapsed_time: float) -> None:
        logger.info(
            "webhook_request_sent",
            headers=self.__header_sanitizer(response.request.headers),
            url=response.url,
            request_body=response.request.content,
            outcome="success" if 200 <= response.status_code <= 299 else "failure",
            elapsed_time=elapsed_time,
        )

    def post(self, payload: Dict) -> Tuple[bool, int]:
        try:
            logger.info("webhook_request_started")
            started_at = perf_counter()
            response = self.client.post(
                url=self.url,
                json=payload,
                timeout=base.HTTP_REQUEST_TIMEOUT,
            )
            response.read()
            self.add_hook_response(response, perf_counter() - started_at)
            response.raise_for_status()
        except (HTTPStatusError, TimeoutException) as exc:
            logger.error("webhook_request_failed", exc_info=str(exc))
            raise
        else:
            try:
                json_response = response.json()
            except json.JSONDecodeError:
                json_response = None

            logger.info(
                "webhook_request_finished",
                status_code=response.status_code,
                json_response=json_response,
            )

            return True, response.status_code
        finally:
            self.client.close()


def webhook_dispatcher(meta: Dict, receiver: Dict, body: Dict) -> Any:
    http = HttpClient(meta, receiver)
    return http.post(body)
