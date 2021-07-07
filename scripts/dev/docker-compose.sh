#!/bin/bash -e

script_dir=$(dirname "$(readlink -fm "$0")")
pushd  $script_dir

source ./load-secrethub-credentials.sh

project_root=$(dirname "$(dirname "$script_dir")")

pushd "$project_root" || (echo 'Failed to push directory on terminal stack.' && exit 1)

# stop and delete previous instances
docker compose stop
if ! [[ -z ${REBUILD+x} ]]; then
    docker compose build --no-cache
fi
# re-create containers
docker compose up -V --force-recreate --remove-orphans --build --abort-on-container-exit "$@"