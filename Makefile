# This makefile is used as an entrypoint for useful scripts (dev, test, etc)
PWD := ${CURDIR}
ARGS :=
TAG := latest
ENVS :=
DOCKER_SOCKET := /var/run/docker.sock
DEFAULT_ENVS := DOCKER_SCAN_SUGGEST=false
INTEGRATION_TESTS_PATH := tests.integration
UNIT_TESTS_PATH := tests.unit
SECRETHUB_CREDENTIAL := $(shell ./scripts/dev/load-secrethub-credentials.sh )

build:
	${ENVS} docker build -t petrci1/adaptive_learning_backend:${TAG} ${ARGS} .

dev : secrethub
	${ENVS} ./scripts/dev/docker-compose.sh ${ARGS}

shell : secrethub
	exec 5>&1 && docker run -it --rm -v ${DOCKER_SOCKET}:${DOCKER_SOCKET} -v  ${PWD}:/app $$(${ENVS} ${DEFAULT_ENVS} docker build --target dev -q $(ARGS) . | tee /dev/fd/5) bash

unittest : 
	TESTS_PATH=${UNIT_TESTS_PATH} SECRETHUB_CREDENTIAL=${SECRETHUB_CREDENTIAL} docker compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web

integrationtest : 
	TESTS_PATH=${INTEGRATION_TESTS_PATH} SECRETHUB_CREDENTIAL=${SECRETHUB_CREDENTIAL} docker compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web

alltest : 
	SECRETHUB_CREDENTIAL=${SECRETHUB_CREDENTIAL} docker compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web
	

