#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py test
gunicorn --bind 0.0.0.0:8888 auction_core.wsgi