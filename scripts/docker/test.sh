#!/bin/bash -ex

BASEDIR=$(dirname "$0")
PROJECT_ROOT=$(dirname $(dirname "$BASEDIR"))
pushd $PROJECT_ROOT

cc-test-reporter before-build                                               # run before-build hook
secrethub run -- coverage run --source='.' manage.py test $TESTS_PATH --noinput # run the tests
test_ecode=$?                                                                 # save last command exit code
secrethub run -- coverage xml                                                 # output xml
cc-test-reporter after-build --exit-code "$test_ecode"                      # run after build

popd