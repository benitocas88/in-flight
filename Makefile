COMPOSE_FILE = docker compose

.PHONY: build
build:
	$(COMPOSE_FILE) build

.PHONY: stop
stop:
	$(COMPOSE_FILE) stop

.PHONY: rm
rm: stop
	docker rm $(shell docker ps -aq --filter name="fli*")

.PHONY: console
console:
	$(COMPOSE_FILE) exec flight bash

.PHONY: up
up: build
	$(COMPOSE_FILE) up -d --remove-orphans

.PHONY: logs
logs:
	$(COMPOSE_FILE) logs -f

.PHONY: run-linting
run-linting:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-linting.sh $(fix)

.PHONY: run-typer
run-typer:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-typer.sh

.PHONY: run-tests
run-tests:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-tests.sh $(name)

.PHONY: run-deps
run-deps:
	$(COMPOSE_FILE) run --rm --no-deps \
		--user "$(shell id -u):$(shell id -g)" \
		--env HOME=/home/in-flight \
		--env PIP_NO_CACHE_DIR=1 \
		--volume "$(CURDIR)/scripts:/opt/scripts:ro" \
		--volume "$(CURDIR)/requirements:/opt/requirements:rw" \
		--workdir /opt/requirements \
		flight bash /opt/scripts/run-deps.sh $(args)

.PHONY: down
down:
	$(COMPOSE_FILE) down --remove-orphans
