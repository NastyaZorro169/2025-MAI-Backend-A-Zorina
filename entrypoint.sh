#!/bin/bash
set -e

cd /app/booksearch
python manage.py migrate
python manage.py collectstatic --noinput

exec gunicorn booksearch.wsgi:application --bind 0.0.0.0:8000