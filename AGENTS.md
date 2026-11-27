# AI agent guidance

## Project

This is a Flask and Celery learning project that we are improving incrementally.
Python source is under `src/`, tests are under `tests/`, and Celery is configured
to use SQS as its message broker.

## Working rules

- Never include `Co-authored-by` trailers or AI attribution in commit messages or
  pull request descriptions.
- Keep changes small and focused; preserve existing behavior unless a change is
  explicitly requested.
- Before changing a Celery task, check its callers, payload, retry behavior, and
  configuration.
- Add or update focused tests for behavior changes. Use the conventions in
  `pyproject.toml`.
- Add clear type annotations to classes, functions, and methods. Keep types
  precise and avoid untyped code.
- Add short, plain-language docstrings to classes and functions when their
  purpose or flow is not obvious. Do not add long docstrings for simple code.
- Never put credentials or other secrets in code, tests, logs, or documentation.
