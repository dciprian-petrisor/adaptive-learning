#!/usr/bin/env bash

set -v
set -x

apt install --yes curl # required to download test reporter
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 >./cc-test-reporter
chmod +x ./cc-test-reporter                                                                           # make it executable
./cc-test-reporter before-build                                                                       # run before-build hook
secrethub --debug run -- conda run --no-capture-output -n adaptive_learning coverage run --source='.' manage.py test --noinput # run the tests
test_ecode=$?                                                                                         # save last command exit code
secrethub --debug run -- conda run --no-capture-output -n adaptive_learning coverage xml                                       # output xml
./cc-test-reporter after-build --exit-code "$test_ecode"                                              # run after build
