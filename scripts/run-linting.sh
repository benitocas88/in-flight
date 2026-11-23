#!/usr/bin/env bash

set -e
set -o errexit

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

cd /home/in-flight

if [ "${1:-}" = "yes" ]
then
    echo -e "${RED}Running${NC} Ruff to fix lint issues and sort imports..."
    ruff check --config /opt/project/pyproject.toml --fix app/
    echo -e "${RED}Running${NC} Ruff to format Python code..."
    ruff format --config /opt/project/pyproject.toml app/
else
    echo -e "${GREEN}Checking${NC} lint issues and import sorting with Ruff..."
    ruff check --config /opt/project/pyproject.toml app/
    echo -e "${GREEN}Checking${NC} Python formatting with Ruff..."
    ruff format --config /opt/project/pyproject.toml --check app/
fi
