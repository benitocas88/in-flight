# In-Flight

## Run the worker

Make sure `.env.local` is set up, then build the Docker images:

```sh
make build
```

Start the services and Celery worker in the background:

```sh
make up
```

Follow the service logs:

```sh
make logs
```

Stop and remove the services:

```sh
make down
```

## Update dependencies

The dependency commands use the existing `in/flight:latest` image. On first
use, build it with the current `uv.lock`:

```sh
make build
```

After changing dependencies in `pyproject.toml`, run these commands in order:

```sh
make lock
make sync-deps
make build
```

`make lock` refreshes `uv.lock`. `make sync-deps` installs from that lockfile
inside Docker. `make build` then puts those dependencies in the worker image.
`uv sync` can also update a stale lockfile, but running `make lock` first makes
the order clear.

To upgrade dependencies allowed by the version pins in `pyproject.toml` and
refresh the lockfile, run:

```sh
make upgrade-deps
```

Exact version pins in `pyproject.toml` must be changed before those direct
dependencies can upgrade.

Review the `pyproject.toml` and `uv.lock` changes together. Docker builds use
the lockfile to install the worker's dependencies.

## Formatting and linting

Run lint checks with:

```sh
make run-linting
```

Apply fixes with:

```sh
make run-linting fix=yes
```
