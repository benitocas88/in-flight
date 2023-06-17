#!/usr/bin/env sh

set -o errexit
set -x
awslocal sqs --endpoint-url=http://localhost:4567 create-queue --queue-name in-flight
set +x
