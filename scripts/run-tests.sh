#!/usr/bin/env bash

set -e
set -o errexit

GREEN='\33[0;32m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

cd /home/pingook

if [ "$1" != "" ]
then
    echo -e "${NC}Running${RED} ONLY ${NC}tests matching ${BOLD}'$1'..."
    pytest -k "$1" app/tests/
else
    echo -e "${NC}Running${GREEN} ALL ${NC}tests..."
    pytest app/tests/
fi
