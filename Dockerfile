FROM python:3.10-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        libpq-dev gcc postgresql-dev python3-dev

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1