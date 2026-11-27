#!/usr/bin/env bash

set -e
set -o errexit

cd /home/in-flight
mypy --config-file /home/in-flight/mypy.ini app/
