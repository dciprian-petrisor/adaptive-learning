FROM continuumio/miniconda3 AS build
WORKDIR /conda
SHELL ["/bin/bash", "-c"]
RUN apt install curl --yes
RUN curl https://apt.secrethub.io | bash
COPY conda_env.yml /conda/
RUN conda env create -f conda_env.yml
WORKDIR /app
COPY . /app/
RUN chmod +x *.sh

FROM continuumio/miniconda3
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN apt install curl --yes
RUN curl https://apt.secrethub.io | bash
COPY --from=build /opt/conda/envs /opt/conda/envs
COPY --from=build /app /app
RUN rm -rf /app/tests
ENV DJANGO_SECRET_KEY=secrethub://petrci1/adaptive_learning_backend/dev/django_secret_key
CMD ["./run.sh"]