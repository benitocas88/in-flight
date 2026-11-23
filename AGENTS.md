# AI agent guidance

## Project

This is a Flask and Celery learning project that we are improving incrementally.
Python source is under `src/`, tests are under `tests/`, and Celery is configured
to use SQS and S3. Local development uses LocalStack.

## Working rules

- Keep changes small and focused; preserve existing behavior unless a change is
  explicitly requested.
- Before changing a Celery task, check its callers, payload, retry behavior, and
  configuration.
- Add or update focused tests for behavior changes. Use the conventions in
  `pyproject.toml`.
- Never put credentials or other secrets in code, tests, logs, or documentation.
- Do not add co-author trailers to commit messages.
