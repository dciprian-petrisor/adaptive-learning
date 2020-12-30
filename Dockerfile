FROM continuumio/miniconda3 AS build
WORKDIR /conda
COPY conda_env.yml /conda/
RUN conda env create -f conda_env.yml

FROM continuumio/miniconda3
COPY  --from=build /opt/conda/envs /opt/conda/envs
WORKDIR /app
COPY . /app/
SHELL ["/bin/bash", "-c"]
CMD ["./run.sh"]