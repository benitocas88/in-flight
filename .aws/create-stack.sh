#!/bin/sh

set -eu

queue_endpoint="${AWS_EMULATOR_ENDPOINT:-https://127.0.0.1:9297}"
last_error="$(mktemp)"
trap 'rm -f "$last_error"' 0

attempt=0
while [ "$attempt" -lt 60 ]; do
    if aws --endpoint-url "$queue_endpoint" --region us-east-2 sqs create-queue \
        --queue-name in-flight \
        --attributes '{"VisibilityTimeout":"300"}' \
        >/dev/null 2>"$last_error"; then
        break
    fi

    attempt=$((attempt + 1))
    sleep 1
done

if [ "$attempt" -eq 60 ]; then
    cat "$last_error" >&2
    echo "Timed out creating the in-flight SQS queue in AWS Emulator." >&2
    exit 1
fi

echo "Ensured the standard in-flight SQS queue has a 300-second visibility timeout."
