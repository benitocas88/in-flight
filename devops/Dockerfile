FROM --platform=linux/amd64 python:3.12.0-slim as base

LABEL maintainer="beni522@gmail.com"

ARG REQUIREMENTS=production

ENV PATH /home/in-flight/.local/bin:$PATH
ENV PYTHONPATH /home/in-flight/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYCURL_SSL_LIBRARY openssl

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    gcc \
    libcurl4-openssl-dev \
    libssl-dev \
    libpython3-dev && \
rm -rf /var/lib/apt/lists/*

RUN useradd in-flight -ms /bin/bash
USER in-flight

WORKDIR /home/in-flight/app

COPY ./requirements /opt/requirements

RUN python -m pip install -U pip --disable-pip-version-check && python -m pip install --no-cache-dir pip-tools
RUN pip-sync /opt/requirements/base.txt /opt/requirements/${REQUIREMENTS}.txt --pip-args "--no-cache-dir --no-deps"

COPY --chown=in-flight:in-flight ./src .

CMD celery -A app.celery worker --loglevel=INFO -E -Ofair --pidfile /tmp/celery.pid
