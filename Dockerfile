FROM python:3.8.7-slim-buster as base

WORKDIR /app
ENV DOCKER=1
ENV PATH=${PATH}:/root/.poetry/bin
COPY ./poetry.lock ./pyproject.toml /app/
RUN apt update -y \
    && apt install -y --no-install-recommends curl ca-certificates \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --no-modify-path \
    && curl https://apt.secrethub.io | bash \
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/* \
    && poetry install --no-dev --no-interaction --no-ansi 

FROM base as dev

ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/dev/django_secret_key

RUN poetry install --no-interaction --no-ansi

VOLUME ["/app"]

CMD ["./scripts/docker/run-dev.sh"]

FROM base as prod

ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/prod/django_secret_key
COPY ./ /app/
RUN rm -rf /app/tests
CMD ["./scripts/docker/run-prod.sh"]

FROM dev as test

ENV TESTS_PATH = ""
RUN apt update -y \
    && apt install -y --no-install-recommends git \
    && curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter \
    && chmod +x cc-test-reporter
COPY ./ /app/
CMD ./scripts/docker/test.sh