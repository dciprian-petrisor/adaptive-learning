#!/usr/bin/env bash

set -e
set -v
set -x

# build the nginx image
docker buildx build --cache-from=type=local,src=/tmp/.buildx-cache --cache-to=type=local,dest=/tmp/.buildx-cache-new -t "${NGINX_IMAGE_NAME}":"${NGINX_IMAGE_TAG}" ./docker/nginx
# build the postgres image
docker buildx build --cache-from=type=local,src=/tmp/.buildx-cache --cache-to=type=local,dest=/tmp/.buildx-cache-new -t "${POSTGRES_IMAGE_NAME}":"${POSTGRES_IMAGE_TAG}" ./docker/postgres
# build the app, up to the build stage only
docker buildx build --cache-from=type=local,src=/tmp/.buildx-cache --cache-to=type=local,dest=/tmp/.buildx-cache-new --target build  -t "${IMAGE_NAME}":"${IMAGE_TAG}"-builder .
