#!/bin/sh

sleep 5

python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic --noinput

exac "$@"