FROM python:3.8.7-slim-buster AS build
WORKDIR /poetry
SHELL ["/bin/bash", "-c"]
RUN apt update --yes
RUN apt install curl --yes
RUN apt install libpq-dev --yes
RUN apt install gcc --yes
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN curl https://apt.secrethub.io | bash
COPY poetry.lock /poetry/
COPY pyproject.toml /poetry/
RUN ~/.poetry/bin/poetry install
WORKDIR /app
COPY . /app/
RUN chmod +x *.sh

FROM python:3.8.7-slim-buster
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN apt update --yes
RUN apt install curl --yes
RUN curl https://apt.secrethub.io | bash
COPY --from=build /root/.poetry /root/.poetry
COPY --from=build /root/.cache /root/.cache
COPY --from=build /app /app
RUN rm -rf /app/tests
ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/dev/django_secret_key
CMD ["./run.sh"]