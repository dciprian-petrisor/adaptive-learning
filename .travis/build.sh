#!/usr/bin/env bash

set -e
set -v
set -x

if ! [[ "$TRAVIS_COMMIT_MESSAGE" =~ .*\[skip-cache\].* ]];
then
  # try to pull the latest build layer image for this branch, to speed up builds
  docker pull "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder || true;
fi ;

# build the nginx image; tag it as NGINX_IMAGE_TAG
docker build -t "${NGINX_IMAGE_NAME}":"${NGINX_IMAGE_TAG}" ./nginx
# build he postgres image; tag it as POSTGRES_IMAGE_TAG
docker build -t "${POSTGRES_IMAGE_NAME}":"${POSTGRES_IMAGE_TAG}" ./postgres
# build only the build stage using the image pulled above as cache; tag it as IMAGE_TAG-builder (which is just git tag + '-builder')
docker build --target build --cache-from "${IMAGE_NAME}":"${TRAVIS_BRANCH}"-builder -t "${IMAGE_NAME}":"${IMAGE_TAG}"-builder .
# print all images (for debugging)
docker images
# push the builder image for this commit to docker
docker push "${IMAGE_NAME}":"${IMAGE_TAG}"-builder # push newly created builder image for test stage
# push the nginx image for this commit to docker
docker push "${NGINX_IMAGE_NAME}":"${NGINX_IMAGE_TAG}"
# push the postgres image for this commit to docker
docker push "${POSTGRES_IMAGE_NAME}":"${POSTGRES_IMAGE_TAG}"