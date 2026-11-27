COMPOSE_FILE = docker compose
UV_IMAGE = in/flight:latest
UV_DOCKER = docker run --rm \
	--user "$(shell id -u):$(shell id -g)" \
	--env HOME=/tmp \
	--env UV_PROJECT_ENVIRONMENT=/tmp/uv-project-venv \
	--volume "$(CURDIR):/opt/project:rw" \
	--workdir /opt/project \
	$(UV_IMAGE)

# Refresh the lockfile after changing pyproject.toml.
# Usage: make lock
# Pass extra uv options with: make lock args="--upgrade"
.PHONY: lock
lock:
	$(UV_DOCKER) uv lock $(args)

# Install dependencies in Docker.
# Usage: make sync-deps
# Install dev tools too: make sync-deps args="--group dev"
.PHONY: sync-deps
sync-deps:
	$(UV_DOCKER) uv sync $(args)

# Upgrade dependencies allowed by pyproject.toml.
# Usage: make upgrade-deps
# Upgrade one package: make upgrade-deps args="--upgrade-package flask"
.PHONY: upgrade-deps
upgrade-deps:
	$(UV_DOCKER) uv sync --upgrade $(args)

# Build the Docker images.
# Usage: make build
.PHONY: build
build:
	$(COMPOSE_FILE) build

# Stop running services.
# Usage: make stop
.PHONY: stop
stop:
	$(COMPOSE_FILE) stop

# Stop services and remove matching containers.
# Usage: make rm
.PHONY: rm
rm: stop
	docker rm $(shell docker ps -aq --filter name="fli*")

# Open a shell in the running flight service.
# Usage: make console
.PHONY: console
console:
	$(COMPOSE_FILE) exec flight bash

# Build images and start services.
# Usage: make up
.PHONY: up
up: build
	$(COMPOSE_FILE) up -d --remove-orphans

# Follow service logs.
# Usage: make logs
.PHONY: logs
logs:
	$(COMPOSE_FILE) logs -f

# Run lint checks. Set fix=--fix to apply fixes.
# Usage: make run-linting
# Apply fixes: make run-linting fix=--fix
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

# Run the type checker.
# Usage: make run-typer
.PHONY: run-typer
run-typer:
	docker run --rm \
		--volume "$(CURDIR)/src:/home/in-flight/app:ro" \
		--volume "$(CURDIR)/mypy.ini:/home/in-flight/mypy.ini:ro" \
		--volume "$(CURDIR)/scripts/run-typer.sh:/opt/scripts/run-typer.sh:ro" \
		--workdir /home/in-flight \
		$(UV_IMAGE) sh /opt/scripts/run-typer.sh

# Run tests. Set name to select a test.
# Usage: make run-tests
# Run one test: make run-tests name=tests/test_orders.py
.PHONY: run-tests
run-tests:
	$(COMPOSE_FILE) run --rm flipys sh /opt/scripts/run-tests.sh $(name)

# Regenerate the lockfile (same as make lock).
# Usage: make run-deps
# Pass uv options: make run-deps args="--upgrade"
.PHONY: run-deps
run-deps: lock

# Stop and remove services and networks.
# Usage: make down
.PHONY: down
down:
	$(COMPOSE_FILE) down --remove-orphans
