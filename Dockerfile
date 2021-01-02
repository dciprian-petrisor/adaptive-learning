FROM continuumio/miniconda3 AS build
WORKDIR /conda
SHELL ["/bin/bash", "-c"]
COPY conda_env.yml /conda/
RUN conda env create -f conda_env.yml
WORKDIR /app
COPY . /app/
RUN chmod +x *.sh

FROM continuumio/miniconda3
WORKDIR /app
SHELL ["/bin/bash", "-c"]
COPY --from=build /opt/conda/envs /opt/conda/envs
COPY --from=build /app /app
RUN rm -rf /app/tests
CMD ["./run.sh"]