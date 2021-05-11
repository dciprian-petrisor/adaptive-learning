#!/bin/bash -e

script_dir=$(dirname "$(readlink -fm "$0")")
pushd  $script_dir

source ./load-secrethub-credentials.sh

project_root=$(dirname "$(dirname "$script_dir")")

pushd "$project_root" || (echo 'Failed to push directory on terminal stack.' && exit 1)

docker compose up "$@"