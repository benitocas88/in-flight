#!/usr/bin/env bash

set -euo pipefail

project_dir="$(mktemp -d)"
cp /opt/project/pyproject.toml /opt/project/uv.lock "$project_dir/"
cd "$project_dir"

printf 'Locking project dependencies with uv...\n'
uv lock "$@"
cat uv.lock > /opt/project/uv.lock
