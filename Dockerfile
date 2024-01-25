FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY ./docker/pyproject.toml /app/pyproject.toml
COPY ./docker/entrypoint.sh /app/entrypoint.sh

RUN apt update \
    && pip install poetry \
    && apt install -y vim \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /app \
    && chdir /app \
    && poetry config virtualenvs.create false \
    && poetry install --only main

COPY --chown=app:app . /app

WORKDIR /app/src

EXPOSE 8000

USER app

CMD ["sh", "/app/entrypoint.sh"]
