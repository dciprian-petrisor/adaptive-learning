FROM python:3.8.7-slim-buster as build

SHELL ["/bin/bash", "-c"] 
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/
RUN apt update -y \
    && apt install -y --no-install-recommends curl libc6-dev libpq-dev gcc ca-certificates \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
    && curl https://apt.secrethub.io | bash \
    && source /root/.profile \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && apt remove -y libc6-dev gcc \
    && rm -rf /var/lib/apt/lists/*
COPY ./ /app/
RUN find . -type f -iname "*.sh" -exec chmod +x {} \;

FROM build as dev
WORKDIR /app

ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/dev/django_secret_key

CMD ["./scripts/docker/run-dev.sh"]

FROM build as prod

ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/prod/django_secret_key
RUN rm -rf /app/tests

CMD ["./scripts/docker/run-prod.sh"]