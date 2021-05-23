#!/bin/bash -e

BASEDIR=$(dirname "$0")
PROJECT_ROOT=$(dirname $(dirname "$BASEDIR"))
pushd $PROJECT_ROOT

export VIRTUAL_ENV="/app/.venv"
python3 -m venv $VIRTUAL_ENV
export PATH="$VIRTUAL_ENV/bin:$PATH"

apt update -y
apt install -y --no-install-recommends git  # required to download test reporter
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 >./cc-test-reporter
chmod +x ./cc-test-reporter                                                   # make it executable
./cc-test-reporter before-build                                               # run before-build hook
secrethub run -- coverage run --source='.' manage.py test $TESTS_PATH --noinput # run the tests
test_ecode=$?                                                                 # save last command exit code
secrethub run -- coverage xml                                                 # output xml
./cc-test-reporter after-build --exit-code "$test_ecode"                      # run after build
