#!/usr/bin/env bash

set -e
set -v
set -x

# pull build & test image for this commit
docker pull "${IMAGE_NAME}":"${IMAGE_TAG}"-builder
# pull the nginx image for this commit
docker pull "${NGINX_IMAGE_NAME}":"${NGINX_IMAGE_TAG}"
# pull the postgres image for this commit
docker pull "${POSTGRES_IMAGE_NAME}":"${POSTGRES_IMAGE_TAG}"
# adding builder to the image tag utilized in the docker-compose.yml, so our image contains the tests as well
IMAGE_TAG="${IMAGE_TAG}-builder"
# start dependent services
docker-compose up -d postgres
docker-compose up -d --no-deps nginx
# run the tests via docker compose, overriding the image tag so we use the builder image pulled above, which contains the tests.
docker-compose run --use-aliases -e TRAVIS_PULL_REQUEST_BRANCH -e TRAVIS_BRANCH -e TRAVIS_PULL_REQUEST_SHA -e TRAVIS_COMMIT -e CC_TEST_REPORTER_ID="${CC_TEST_REPORTER_ID}" --rm web ./test.sh
# set the image back to what it was
IMAGE_TAG=${IMAGE_TAG//-builder/}
# here, all tests passed, so we can tag this image as the new base builder image for subsequent builds for this branch
docker tag "${IMAGE_NAME}":"${IMAGE_TAG}"-builder "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder
# print images for debugging purposes
docker images
# push the new builder image for this branch, since build & tests passed and it is valid.
docker push "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder
