#!/usr/bin/env sh

set -o errexit
set -x
awslocal s3api --endpoint-url=http://localhost:4567 create-bucket --bucket in-flight
set +x
