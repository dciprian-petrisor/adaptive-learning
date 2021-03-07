FROM python:3.8.7-slim-buster AS build
WORKDIR /poetry
RUN apt update -y && apt install curl libc6-dev libpq-dev gcc -y && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN curl https://apt.secrethub.io | bash
SHELL ["/bin/bash", "-lc"]
WORKDIR /app
COPY . /app/
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi
RUN chmod +x *.sh

FROM python:3.8.7-slim-buster
WORKDIR /app
ENV VIRTUAL_ENV="/app/.venv"
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/dev/django_secret_key
RUN apt update -y && apt install curl libpq-dev -y && rm -rf /var/lib/apt/lists/*
RUN curl https://apt.secrethub.io | bash
COPY --from=build /app /app
RUN rm -rf /app/tests

CMD ["./run.sh"]