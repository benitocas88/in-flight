from flight.settings.base import env

S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", default=None)


class S3Backend:
    result_backend = env.str("S3_RESULT_BACKEND", default="s3://")

    s3_region = env.str("AWS_S3_REGION_NAME", default="us-east-2")
    s3_bucket = env.str("AWS_S3_BUCKET_NAME", default="in-flight")
    s3_base_path = env.str("AWS_S3_BUCKET_PATH", default="backend-results/")

    if S3_ENDPOINT_URL:
        s3_endpoint_url = S3_ENDPOINT_URL
