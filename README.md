# In-Flight

## Updating dependencies

Declare runtime dependencies in `[project].dependencies` and development-only
dependencies in `[dependency-groups].dev` in `pyproject.toml`.

After editing dependencies, regenerate the committed lockfile with:

```sh
make build
make run-deps
```

`make run-deps` runs `uv lock` inside the project Docker image and updates
`uv.lock` in the working tree. Build the image first so the target has the
`in/flight:latest` image available. The target does not install dependencies
on the host.

To refresh all locked versions or a specific package, pass uv options through
Make:

```sh
make run-deps args=--upgrade
make run-deps args="--upgrade-package flask"
```

Review and commit the `pyproject.toml` and `uv.lock` changes together. Docker
builds install runtime dependencies by default; the Compose development image
also installs the `dev` dependency group.

## Formatting and linting

Ruff handles linting, import sorting, and formatting. Run checks with:

```sh
make run-linting
```

Apply safe lint fixes, sort imports, and format the source with:

```sh
make run-linting fix=yes
```
