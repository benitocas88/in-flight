FROM python:3.15.2-trixie AS base
COPY --link --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /usr/local/bin/

LABEL maintainer="beni522@gmail.com"

ARG INSTALL_DEV_DEPENDENCIES=0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYCURL_SSL_LIBRARY=openssl \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

RUN useradd --create-home --shell /bin/bash in-flight

WORKDIR /home/in-flight/app

COPY pyproject.toml uv.lock ./

RUN if [ "${INSTALL_DEV_DEPENDENCIES}" = "1" ]; then \
        uv sync --locked --group dev; \
    else \
        uv sync --locked --no-dev; \
    fi

USER in-flight

COPY --chown=in-flight:in-flight ./src .

CMD ["celery", "-A", "app.celery", "worker", "--loglevel=INFO"]
