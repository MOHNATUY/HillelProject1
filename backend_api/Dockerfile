FROM python:3.12-slim

WORKDIR /app

ENV POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-ansi --no-root --no-interaction

COPY /app /app

EXPOSE 2323
