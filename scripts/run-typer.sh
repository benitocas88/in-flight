#!/usr/bin/env bash

set -e
set -o errexit

cd /home/pingook
mypy app/
