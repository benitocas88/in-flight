from flight.settings.base import env


class SQS:
    broker_transport_options = {
        "region": env.str("AWS_SQS_REGION_NAME", default="us-east-2"),
        "is_secure": env.bool("AWS_SQS_TRANSPORT_SECURE", default=True),
    }
