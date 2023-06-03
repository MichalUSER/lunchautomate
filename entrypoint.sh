#!/usr/bin/env bash

set -o errexit

python manage.py collectstatic  --noinput
python manage.py migrate  --noinput

gunicorn --bind :8000 --workers 2 lunchautomate.wsgi