FROM python:3.15.2-trixie AS base
COPY --link --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /usr/local/bin/

LABEL maintainer="beni522@gmail.com"

ARG REQUIREMENTS=production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYCURL_SSL_LIBRARY=openssl \
    UV_COMPILE_BYTECODE=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        gcc \
        libcurl4-openssl-dev \
        libssl-dev \
        libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash in-flight

WORKDIR /home/in-flight/app

RUN --mount=type=bind,source=requirements,target=/opt/requirements \
    uv pip sync --system --no-cache \
        /opt/requirements/base.txt /opt/requirements/${REQUIREMENTS}.txt

USER in-flight

COPY --chown=in-flight:in-flight ./src .

CMD ["celery", "-A", "app.celery", "worker", "--loglevel=INFO"]
