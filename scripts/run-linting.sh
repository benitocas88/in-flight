#!/usr/bin/env bash

set -e
set -o errexit

GREEN='\33[0;32m'
RED='\033[0;31m'
NC='\033[0m'

cd /home/pingook

if [ "$1" = "yes" ]
then
    echo -e "${RED}Running${NC} pycln to remove unused imports..."
    pycln app/ --all
    echo -e "${RED}Running${NC} isort to sort imports..."
    isort app/
    echo -e "${RED}Running${NC} black to format python code..."
    black app/
else
    echo -e "${GREEN}Running${NC} pycln to check for unused imports..."
    pycln app/ --check --all
    echo -e "${GREEN}Running${NC} isort to check for imports ordering..."
    isort --check-only -d app/
    echo -e "${GREEN}Running${NC} black to check python formatting..."
    black --check app/
fi
