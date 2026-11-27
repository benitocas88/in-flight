import os
from uuid import uuid4

from flask.app import Flask

from flight.celery.app import make_celery
from flight.settings.base import env

conf = os.path.join(
    os.path.dirname(__file__),
    "flight",
    "settings",
    env.str("ENV_FILENAME"),
)

app = Flask(__name__)
app.config.from_pyfile(conf)

celery = make_celery(app)


@app.cli.command("test")
def test() -> None:
    import time

    while True:
        request_id = uuid4().hex
        celery.send_task(
            "orders.notify_payment_status",
            kwargs={
                "meta": {"request_id": request_id},
                "webhook": {
                    "receiver": {
                        "url": "https://webhook.site/92a71e0f-b81b-4f62-b8ab-2822c350759d",
                        "auth": {
                            "key": "Bearer",
                            "value": (
                                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
                                "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
                            ),
                        },
                    },
                    "body": {
                        "data": {
                            "order_id": "A-2023/01",
                            "payment": {"authorization_code": None, "status": "rejected"},
                            "created_at": 1687737170,
                        },
                    },
                },
            },
        )
        print("message sent...")
        time.sleep(7)
