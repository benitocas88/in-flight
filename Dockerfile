FROM python:3.12.1-bookworm AS base

LABEL maintainer="beni522@gmail.com"

ARG REQUIREMENTS=production

ENV PATH="/home/in-flight/.local/bin:${PATH}" \
    PYTHONPATH="/home/in-flight/app" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYCURL_SSL_LIBRARY=openssl

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        gcc \
        libcurl4-openssl-dev \
        libssl-dev \
        libpython3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash in-flight
USER in-flight

WORKDIR /home/in-flight/app

RUN --mount=type=bind,source=requirements,target=/opt/requirements \
    python -m pip install --no-cache-dir --disable-pip-version-check pip-tools \
    && pip-sync /opt/requirements/base.txt /opt/requirements/${REQUIREMENTS}.txt \
        --pip-args="--no-cache-dir --no-deps"

COPY --chown=in-flight:in-flight ./src .

CMD ["celery", "-A", "app.celery", "worker", "--loglevel=INFO"]
