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
up: build external-net
	$(COMPOSE_FILE) up -d --remove-orphans

up-dd:
	$(COMPOSE_FILE) --profile dd-agent up -d --remove-orphans

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
	$(COMPOSE_FILE) run --rm -it flipys sh /opt/scripts/run-deps.sh $(args)

.PHONY: external-net
external-net: SERVICE_GRP_NET=service-grp-net
external-net: ## Create common external docker network (if missing).
	@if [ "$$(docker network ls --filter name=$(SERVICE_GRP_NET) --format '{{ .Name }}')" != $(SERVICE_GRP_NET) ]; then \
		docker network create $(SERVICE_GRP_NET); \
	fi

.PHONY: down
down:
	$(COMPOSE_FILE) down --remove-orphans
