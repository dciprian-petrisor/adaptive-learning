#!/usr/bin/env bash

set -e
set -v
set -x

# setting the image name for the docker-compose command
IMAGE_TAG="${IMAGE_TAG}-builder"
# start dependent services
docker-compose up -d postgres
docker-compose up -d --no-deps nginx
# run the tests via docker compose
docker-compose run --use-aliases -e SECRETHUB_CREDENTIAL -e GIT_BRANCH -e GIT_COMMIT_SHA -e CC_TEST_REPORTER_ID --rm web ./scripts/docker/test.sh
# set the image back to what it was
IMAGE_TAG=${IMAGE_TAG//-builder/}