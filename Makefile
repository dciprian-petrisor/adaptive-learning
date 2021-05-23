# This makefile is used as an entrypoint for useful scripts (dev, test, etc)
PWD := ${CURDIR}
ARGS :=
TAG := latest
ENVS :=
DOCKER_SOCKET := /var/run/docker.sock
DEFAULT_ENVS := DOCKER_SCAN_SUGGEST=false
INTEGRATION_TESTS_PATH := tests.integration
UNIT_TESTS_PATH := tests.unit

ifndef SECRETHUB_CREDENTIAL
	SECRETHUB_CREDENTIAL := $(shell ./scripts/dev/load-secrethub-credentials.sh )
endif
export SECRETHUB_CREDENTIAL := ${SECRETHUB_CREDENTIAL}


build:
	${ENVS} docker build -t petrci1/adaptive_learning_backend:${TAG} ${ARGS} .

dev: 
	${ENVS} ./scripts/dev/docker-compose.sh ${ARGS}

shell:
	exec 5>&1 && docker run -it --rm -v ${DOCKER_SOCKET}:${DOCKER_SOCKET} -v  ${PWD}:/app $$(${ENVS} ${DEFAULT_ENVS} docker build --target dev -q $(ARGS) . | tee /dev/fd/5) bash

unittest: 
	TESTS_PATH=${UNIT_TESTS_PATH}  docker-compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web

integrationtest: 
	TESTS_PATH=${INTEGRATION_TESTS_PATH}  docker-compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web

alltest: 
	docker-compose -f docker-compose.test.yml up -V --force-recreate --remove-orphans --build --abort-on-container-exit --exit-code-from web
	

