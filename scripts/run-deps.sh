#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../requirements"

for requirement in base all production; do
    printf 'Compiling %s.in -> %s.txt\n' "$requirement" "$requirement"
    pip-compile -q "$@" "${requirement}.in" \
        --resolver=backtracking \
        --no-strip-extras \
        --output-file="${requirement}.txt"
done
