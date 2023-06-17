from datetime import datetime, timedelta

from flight.settings.base import env


class BaseBackend:
    result_expires = datetime.utcnow() + timedelta(
        seconds=env.int("RESULT_EXPIRES_IN_SECONDS", default=3600)
    )
