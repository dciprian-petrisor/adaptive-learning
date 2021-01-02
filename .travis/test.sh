#!/usr/bin/env bash

set -e
set -v
set -x

# pull build & test image for this commit
docker pull "${IMAGE_NAME}":"${IMAGE_TAG}"-builder
# adding builder to the image tag utilized in the docker-compose.yml, so our image contains the tests as well
IMAGE_TAG="${IMAGE_TAG}-builder"
# start nginx as well for integration testing
docker-compose up -d nginx
# run the tests via docker compose, overriding the image tag so we use the builder image pulled above, which contains the tests.
docker-compose run --use-aliases -e CC_TEST_REPORTER_ID="${CC_TEST_REPORTER_ID}" -e TRAVIS_TEST_RESULT="${TRAVIS_TEST_RESULT}" --rm web ./test.sh
# set the image back to what it was
IMAGE_TAG=${IMAGE_TAG//-builder/}
# here, all tests passed, so we can tag this image as the new base builder image for subsequent builds for this branch
docker tag "${IMAGE_NAME}":"${IMAGE_TAG}"-builder "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder
# push the new builder image for this branch, since build & tests passed and it is valid.
docker push "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder
