#!/usr/bin/env bash
set -e

conda run --no-capture-output -n adaptive_learning python resillient_migrate.py
conda run --no-capture-output -n adaptive_learning python manage.py runserver 0.0.0.0:8000