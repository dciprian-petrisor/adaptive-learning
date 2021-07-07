#!/bin/bash -e


BASEDIR=$(dirname "$0")
PROJECT_ROOT=$(dirname $(dirname "$BASEDIR"))
pushd $PROJECT_ROOT
# Name of the application
NAME="backend"
DJANGODIR=/app
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=adaptive_learning.settings
DJANGO_WSGI_MODULE=adaptive_learning.wsgi
echo "Starting $NAME as $(whoami)"
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# migrate
secrethub run -- python resillient_migrate.py
secrethub run -- python manage.py collectstatic --noinput
# Start Django app
secrethub run -- python manage.py runserver 0.0.0.0:8000
