# This makefile is used as an entrypoint for useful scripts (dev, test, etc)
PWD := ${CURDIR}
ARGS :=
TAG := latest
ENVS :=
build:
	${ENVS} docker build -t petrci1/adaptive_learning_backend:${TAG} ${ARGS} .


dev:
	${ENVS} ./scripts/dev/docker-compose.sh ${ARGS}