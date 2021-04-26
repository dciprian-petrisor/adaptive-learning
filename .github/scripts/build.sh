#!/usr/bin/env bash

set -e
set -v
set -x

# build the nginx image
docker build -t "${NGINX_IMAGE_NAME}":"${NGINX_IMAGE_TAG}" ./docker/nginx
# build the postgres image
docker build -t "${POSTGRES_IMAGE_NAME}":"${POSTGRES_IMAGE_TAG}" ./docker/postgres
# build the app, up to the build stage only
docker build --target build  -t "${IMAGE_NAME}":"${IMAGE_TAG}"-builder .