#!/usr/bin/env bash

set -e
set -v
set -x

# try to pull the latest build layer image for this branch, to speed up builds
docker pull "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder || true
# build only the build stage using the image pulled above as cache; tag it as IMAGE_TAG-builder (which is just git tag + '-builder')
docker build --target build --cache-from "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder -t "${IMAGE_NAME}":"${IMAGE_TAG}"-builder .
# print all images (for debugging)
docker images
# push the builder image for this commit to docker
docker push "${IMAGE_NAME}":"${IMAGE_TAG}"-builder # push newly created builder image for test stage
