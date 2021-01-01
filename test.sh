#!/usr/bin/env bash
set -e

apt install --yes curl # required to download test reporter
curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 >./cc-test-reporter
chmod +x ./cc-test-reporter                                                                 # make it executable
./cc-test-reporter before-build                                                             # run before-build hook
conda run --no-capture-output -n adaptive_learning coverage run --source='.' manage.py test # run the tests
conda run --no-capture-output -n adaptive_learning coverage xml                             # output xml
./cc-test-reporter after-build -t coverage.py --exit-code "$TRAVIS_TEST_RESULT"             # run after build
