#!/usr/bin/env bash
set -e
set -v
set -x

# install secret hub
apt install curl --yes
curl https://apt.secrethub.io | bash

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
secrethub run -- conda run --no-capture-output -n adaptive_learning python resillient_migrate.py
secrethub run -- conda run --no-capture-output -n adaptive_learning python manage.py collectstatic --noinput
# Start your Django Unicorn
secrethub run -- conda run --no-capture-output -n adaptive_learning gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=0.0.0.0:8000 \
  --log-level=debug \
  --log-file=-
