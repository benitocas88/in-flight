import json

import httpx

from flight.utils import http as http_module


def test_http_client_posts_json_with_request_and_auth_headers(monkeypatch):
    seen_requests = []

    def handle_request(request):
        seen_requests.append(request)
        return httpx.Response(200, json={"accepted": True})

    transport = httpx.MockTransport(handle_request)
    monkeypatch.setattr(
        http_module,
        "Client",
        lambda **kwargs: httpx.Client(transport=transport, **kwargs),
    )
    client = http_module.HttpClient(
        {"request_id": "request-123"},
        {
            "url": "https://example.com/webhook",
            "auth": {"key": "Authorization", "value": "Bearer token"},
        },
    )

    assert client.post({"event": "created"}) == (True, 200)

    request = seen_requests[0]
    assert request.headers["X-Request-Id"] == "request-123"
    assert request.headers["Authorization"] == "Bearer token"
    assert json.loads(request.content) == {"event": "created"}
