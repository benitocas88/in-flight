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
	docker run --rm \
		--user "$(shell id -u):$(shell id -g)" \
		--env HOME=/tmp \
		--volume "$(CURDIR)/src:/home/in-flight/app:rw" \
		--volume "$(CURDIR)/scripts:/opt/scripts:ro" \
		--volume "$(CURDIR)/pyproject.toml:/opt/project/pyproject.toml:ro" \
		--workdir /home/in-flight \
		in/flight:latest bash /opt/scripts/run-linting.sh $(fix)

.PHONY: run-typer
run-typer:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-typer.sh

.PHONY: run-tests
run-tests:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-tests.sh $(name)

.PHONY: run-deps
run-deps:
	docker run --rm \
		--user "$(shell id -u):$(shell id -g)" \
		--env HOME=/tmp \
		--volume "$(CURDIR)/scripts:/opt/scripts:ro" \
		--volume "$(CURDIR)/pyproject.toml:/opt/project/pyproject.toml:ro" \
		--volume "$(CURDIR)/uv.lock:/opt/project/uv.lock:rw" \
		--workdir /opt/project \
		in/flight:latest bash /opt/scripts/run-deps.sh $(args)

.PHONY: down
down:
	$(COMPOSE_FILE) down --remove-orphans
