FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE="false"

# Install lightweight build tools for any binary Python dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install --no-cache-dir "poetry>=2"

COPY . /package/
WORKDIR /package

RUN poetry install --with sandbox

WORKDIR /app
