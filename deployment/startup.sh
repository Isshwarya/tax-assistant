#!/usr/bin/env bash
set -x
cd /tax_assistant
python manage.py makemigrations; python manage.py migrate

(cd /tax_assistant; gunicorn tax_assistant.wsgi:application --user www-data --bind 0.0.0.0:8000 --workers 3) &
nginx -g "daemon off;"